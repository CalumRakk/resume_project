import logging
from typing import Dict, List, Any, Optional, Type

from rest_framework import serializers
from django.core.validators import EmailValidator
from django.db.models import Model
from django.db import transaction

from .models import Resume, Skill, Experience, Template


logger = logging.getLogger(__name__)


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = ["id", "name", "level", "keywords", "orden"]

    def validate_id(self, value):
        if self.context["request"].method == "POST" and value is not None:
            raise serializers.ValidationError(
                "No se debe proporcionar un ID al crear un Resume."
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
            "orden",
        ]

    def validate_id(self, value):
        if self.context["request"].method == "POST" and value is not None:
            raise serializers.ValidationError(
                "No se debe proporcionar un ID al crear un Resume."
            )
        return value


class TemplateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Template
        fields = ["id", "name", "descripcion", "componet_name", "customazation_rules"]

    def validate(self, attrs):
        logger.info(f"Validando datos de Template: {attrs}")
        return super().validate(attrs)


class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Resume que maneja la creación y actualización de Resume.
    """

    skills: List[Dict[str, Any]] = SkillSerializer(many=True, required=False)
    experiences: List[Dict[str, Any]] = ExperienceSerializer(many=True, required=False)
    template_selected: Optional[int] = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), required=False, write_only=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Resume
        fields = "__all__"
        extra_kwargs = {
            "email": {"validators": [EmailValidator("Ingrese un correo válido.")]},
        }

    def to_representation(self, instance: Resume) -> Dict[str, Any]:
        """
        Convierte una instancia de Resume a su representación JSON.

        Args:
            instance (Resume): Instancia del modelo Resume a serializar.

        Returns:
            Dict[str, Any]: Diccionario con la representación JSON del Resume.
        """
        logger.info(
            f"Convirtiendo instancia de Resume a representación JSON: {instance.id}"
        )
        representation = super().to_representation(instance)

        if instance.template_selected:
            representation["template_selected"] = TemplateSerializer(
                instance.template_selected
            ).data
        return representation

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Resume:
        """
        Crea una nueva instancia de Resume con sus relaciones dentro de una transacción.
        Si ocurre algún error durante la creación de las relaciones, se hace rollback
        de todas las operaciones.

        Args:
            validated_data (Dict[str, Any]): Datos validados para crear el Resume.

        Returns:
            Resume: Nueva instancia del modelo Resume creada.

        Raises:
            ValidationError: Si hay errores en la creación de objetos relacionados.
            DatabaseError: Si hay errores en la base de datos.
        """
        logger.info(f"Iniciando transacción para crear nuevo Resume")
        try:
            # Extraer datos de relaciones
            skills_data = validated_data.pop("skills", [])
            experiences_data = validated_data.pop("experiences", [])

            # Crear el Resume
            resume = Resume.objects.create(**validated_data)

            # Crear relaciones
            self._create_related_objects(resume, experiences_data, skills_data)

            logger.info(f"Resume creado exitosamente: {resume.id}")
            return resume

        except Exception as e:
            logger.error(f"Error durante la creación del Resume: {str(e)}")
            raise

    @transaction.atomic
    def update(self, instance: Resume, validated_data: Dict[str, Any]) -> Resume:
        """
        Actualiza una instancia existente de Resume y sus relaciones dentro de una
        transacción. Si ocurre algún error durante la actualización, se hace rollback
        de todas las operaciones.

        Args:
            instance (Resume): Instancia del modelo Resume a actualizar.
            validated_data (Dict[str, Any]): Datos validados para la actualización.

        Returns:
            Resume: Instancia del modelo Resume actualizada.

        Raises:
            ValidationError: Si hay errores en la actualización de objetos relacionados.
            DatabaseError: Si hay errores en la base de datos.
        """
        logger.info(f"Iniciando transacción para actualizar Resume: {instance.id}")
        try:
            # Extraer datos de relaciones
            skills_data = validated_data.pop("skills", [])
            experiences_data = validated_data.pop("experiences", [])

            # Actualizar campos básicos
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()

            # Actualizar relaciones
            self._update_related_objects(instance, Skill, skills_data)
            self._update_related_objects(instance, Experience, experiences_data)

            logger.info(f"Resume actualizado exitosamente: {instance.id}")
            return instance

        except Exception as e:
            logger.error(f"Error durante la actualización del Resume: {str(e)}")
            raise

    def _create_related_objects(
        self,
        resume: Resume,
        experiences_data: List[Dict[str, Any]],
        skills_data: List[Dict[str, Any]],
    ) -> None:
        """
        Crea los objetos relacionados (experiencias y habilidades) para un Resume.
        Esta función se ejecuta dentro de una transacción controlada por el método create().

        Args:
            resume (Resume): Instancia del modelo Resume.
            experiences_data (List[Dict[str, Any]]): Datos de experiencias a crear.
            skills_data (List[Dict[str, Any]]): Datos de habilidades a crear.

        Raises:
            ValidationError: Si hay errores en los datos proporcionados.
            DatabaseError: Si hay errores en la base de datos.
        """
        for experience_data in experiences_data:
            logger.info(f"Creando Experience para el Resume: {resume.id}")
            Experience.objects.create(resume=resume, **experience_data)

        for skill_data in skills_data:
            logger.info(f"Creando Skill para el Resume: {resume.id}")
            Skill.objects.create(resume=resume, **skill_data)

    def _update_related_objects(
        self,
        instance: Resume,
        model_class: Type[Model],
        objects_data: List[Dict[str, Any]],
    ) -> None:
        """
        Actualiza/reemplaza objetos relacionados (experiencias o habilidades) de un Resume.
        Esta función se ejecuta dentro de una transacción controlada por el método update().

        Args:
            instance (Resume): Instancia del modelo Resume.
            model_class (Type[Model]): Clase del modelo a actualizar (Skill o Experience).
            objects_data (List[Dict[str, Any]]): Datos de los objetos a actualizar.

        Raises:
            ValidationError: Si hay errores en los datos proporcionados.
            DatabaseError: Si hay errores en la base de datos.
        """
        # Nombre de la relación ('skills' o 'experiences').
        related_manager = getattr(instance, model_class.__name__.lower() + "s")

        # Eliminar objetos que no están en los datos recibidos
        request = self.context["request"]
        if request.method == "PUT":
            object_ids = [obj["id"] for obj in objects_data if obj.get("id")]
            logger.info(
                f"Eliminando objetos no proporcionados para el Resume: {instance.id}"
            )
            related_manager.exclude(id__in=object_ids).delete()

        # Actualizar o crear objetos
        for object_data in objects_data:
            object_id = object_data.get("id")
            if object_id:
                try:
                    related_object = related_manager.get(id=object_id)
                    logger.info(
                        f"Actualizando {model_class.__name__} con ID: {object_id}"
                    )
                    for key, value in object_data.items():
                        setattr(related_object, key, value)
                    related_object.save()
                except model_class.DoesNotExist:
                    logger.warning(
                        f"{model_class.__name__} con ID: {object_id} "
                        "no encontrado. Creando nuevo."
                    )
                    related_manager.create(**object_data)
            else:
                logger.info(
                    f"Creando nuevo {model_class.__name__} para el Resume: {instance.id}"
                )
                related_manager.create(**object_data)
