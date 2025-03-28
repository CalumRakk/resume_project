import logging
from typing import Dict, List, Any, Optional, Type

from rest_framework import serializers
from django.core.validators import EmailValidator
from django.db.models import Model
from django.db import transaction
from jsonschema import validate, ValidationError

from .models import Resume, Skill, Experience, Template, ResumeCustomization
from .utils import SchemaLoader


logger = logging.getLogger(__name__)


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = ["id", "name", "level", "keywords"]

    def validate_id(self, value):
        if self.context["request"].method == "POST" and value is not None:
            raise serializers.ValidationError(
                "An ID should not be provided when creating a Resume."
            )
        return value


class ExperienceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Experience
        fields = [
            "id",
            "name",
            "position",
            "url",
            "highlights",
            "summary",
            "start_date",
            "end_date",
        ]

    def validate_id(self, value):
        if self.context["request"].method == "POST" and value is not None:
            raise serializers.ValidationError(
                "An ID should not be provided when creating a Resume."
            )
        return value


class ResumeCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeCustomization
        fields = ["id", "custom_styles"]
        extra_kwargs = {
            "resume": {"required": False},
            "template": {"required": False},
        }


class TemplateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Template
        fields = ["id", "name", "descripcion", "componet_name", "customization_rules"]

    def validate_customization_rules(self, value):
        """Validates customization_rules using JSON Schema loaded into memory."""
        schema = SchemaLoader.load_schema("customization_rules.json")
        try:
            validate(instance=value, schema=schema)
        except ValidationError as e:
            raise serializers.ValidationError(
                f"Error in customization_rules: {e.message}"
            )
        return value


class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Resume model that handles the creation and updating of Resumes.
    """

    skills: List[Dict[str, Any]] = SkillSerializer(many=True, required=False)
    experiences: List[Dict[str, Any]] = ExperienceSerializer(many=True, required=False)
    template_selected: Optional[int] = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), required=False, write_only=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    customization = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = "__all__"
        extra_kwargs = {
            "email": {"validators": [EmailValidator("Enter a valid email.")]},
        }

    def to_representation(self, instance: Resume) -> Dict[str, Any]:
        """
        Converts a Resume instance to its JSON representation.

        Args:
            instance (Resume): Instance of the Resume model to serialize.

        Returns:
            Dict[str, Any]: Dictionary with the JSON representation of the Resume.
        """
        logger.info(f"Converting Resume instance to JSON representation: {instance.id}")
        representation = super().to_representation(instance)

        if instance.template_selected:
            representation["template_selected"] = TemplateSerializer(
                instance.template_selected
            ).data
        return representation

    def get_customization(self, obj) -> ResumeCustomizationSerializer:
        """Returns the customization of a Resume if available."""
        return (
            ResumeCustomizationSerializer(obj.customization).data
            if hasattr(obj, "customization")
            else None
        )

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Resume:
        """
        Creates a new Resume instance with its relationships within a transaction.
        If any error occurs during the creation of the relationships, a rollback is performed
        of all operations.

        Args:
            validated_data (Dict[str, Any]): Validated data to create the Resume.

        Returns:
            Resume: New instance of the created Resume model.

        Raises:
            ValidationError: If there are errors in the creation of related objects.
            DatabaseError: If there are errors in the database.
        """
        logger.info(f"Starting transaction to create new Resume")
        try:
            # TODOS: The creation operation must be optimized, to avoid having to use the Model.create method so many times
            # Extract relationship data
            skills_data = validated_data.pop("skills", [])
            experiences_data = validated_data.pop("experiences", [])

            # Create the Resume
            resume = Resume.objects.create(**validated_data)

            # Create relationships
            self._create_related_objects(resume, experiences_data, skills_data)

            logger.info(f"Resume created successfully: {resume.id}")
            return resume

        except Exception as e:
            logger.error(f"Error during Resume creation: {str(e)}")
            raise

    @transaction.atomic
    def update(self, instance: Resume, validated_data: Dict[str, Any]) -> Resume:
        """
        Updates an existing Resume instance and its relationships within a
        transaction. If any error occurs during the update, a rollback is performed
        of all operations.

        Args:
            instance (Resume): Instance of the Resume model to update.
            validated_data (Dict[str, Any]): Validated data for the update.

        Returns:
            Resume: Updated instance of the Resume model.

        Raises:
            ValidationError: If there are errors in the update of related objects.
            DatabaseError: If there are errors in the database.
        """
        logger.info(f"Starting transaction to update Resume: {instance.id}")
        try:
            # Extract relationship data
            skills_data = validated_data.pop("skills", [])
            experiences_data = validated_data.pop("experiences", [])

            # Update basic fields
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()

            # Update relationships
            self._update_related_objects(instance, Skill, skills_data)
            self._update_related_objects(instance, Experience, experiences_data)

            logger.info(f"Resume updated successfully: {instance.id}")
            return instance

        except Exception as e:
            logger.error(f"Error during Resume update: {str(e)}")
            raise

    def _create_related_objects(
        self,
        resume: Resume,
        experiences_data: List[Dict[str, Any]],
        skills_data: List[Dict[str, Any]],
    ) -> None:
        """
        Creates the related objects (experiences and skills) for a Resume.
        This function is executed within a transaction controlled by the create() method.

        Args:
            resume (Resume): Instance of the Resume model.
            experiences_data (List[Dict[str, Any]]): Data of experiences to create.
            skills_data (List[Dict[str, Any]]): Data of skills to create.

        Raises:
            ValidationError: If there are errors in the provided data.
            DatabaseError: If there are errors in the database.
        """
        for experience_data in experiences_data:
            logger.info(f"Creating Experience for the Resume: {resume.id}")
            Experience.objects.create(resume=resume, **experience_data)

        for skill_data in skills_data:
            logger.info(f"Creating Skill for the Resume: {resume.id}")
            Skill.objects.create(resume=resume, **skill_data)

    def _update_related_objects(
        self,
        instance: Resume,
        model_class: Type[Model],
        objects_data: List[Dict[str, Any]],
    ) -> None:
        """
        Updates/replaces related objects (experiences or skills) of a Resume.
        This function is executed within a transaction controlled by the update() method.

        Args:
            instance (Resume): Instance of the Resume model.
            model_class (Type[Model]): Class of the model to update (Skill or Experience).
            objects_data (List[Dict[str, Any]]): Data of the objects to update.

        Raises:
            ValidationError: If there are errors in the provided data.
            DatabaseError: If there are errors in the database.
        """
        # Name of the relationship ('skills' or 'experiences').
        related_manager = getattr(instance, model_class.__name__.lower() + "s")

        # Delete objects that are not in the received data
        request = self.context["request"]
        if request.method == "PUT":
            object_ids = [obj["id"] for obj in objects_data if obj.get("id")]
            logger.info(f"Deleting objects not provided for the Resume: {instance.id}")
            related_manager.exclude(id__in=object_ids).delete()

        # Update or create objects
        for object_data in objects_data:
            object_id = object_data.get("id")
            if object_id:
                try:
                    related_object = related_manager.get(id=object_id)
                    logger.info(f"Updating {model_class.__name__} with ID: {object_id}")
                    for key, value in object_data.items():
                        setattr(related_object, key, value)
                    related_object.save()
                except model_class.DoesNotExist:
                    logger.warning(
                        f"{model_class.__name__} with ID: {object_id} "
                        "not found. Creating new."
                    )
                    related_manager.create(**object_data)
            else:
                logger.info(
                    f"Creating new {model_class.__name__} for the Resume: {instance.id}"
                )
                related_manager.create(**object_data)
