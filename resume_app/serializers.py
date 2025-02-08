import logging
from rest_framework import serializers
from .models import Resume, Skill, Experience, Template
from django.core.validators import EmailValidator


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
    skills = SkillSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    template_selected = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), required=False, write_only=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    full_name = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        help_text="Nombre completo del candidato.",
    )
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator(message="Ingrese un correo electrónico válido.")],
        help_text="Dirección de correo electrónico del candidato.",
    )
    summary = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        help_text="Resumen profesional del candidato (máximo 500 caracteres).",
    )

    class Meta:
        model = Resume
        fields = "__all__"

    def to_representation(self, instance):
        """
        Sobrescribe la representación para incluir el template_selected como un objeto JSON.
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

    def create(self, validated_data):
        logger.info(f"Creando un nuevo Resume con datos: {validated_data}")
        user = self.context["request"].user
        validated_data["user"] = user

        skills_data = validated_data.pop("skills", [])
        experiences_data = validated_data.pop("experiences", [])
        resume = Resume.objects.create(**validated_data)

        for experience_data in experiences_data:
            logger.info(f"Creando Experience para el Resume: {resume.id}")
            Experience.objects.create(resume=resume, **experience_data)
        for skill_data in skills_data:
            logger.info(f"Creando Skill para el Resume: {resume.id}")
            Skill.objects.create(resume=resume, **skill_data)

        logger.info(f"Resume creado exitosamente: {resume.id}")
        return resume

    def update(self, instance, validated_data):
        logger.info(f"Actualizando el Resume con ID: {instance.id}")
        user = self.context["request"].user
        validated_data["user"] = user

        skills_data = validated_data.pop("skills", [])
        experiences_data = validated_data.pop("experiences", [])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Obtener los IDs de los skills que están en el JSON
        # Eliminar los skills que no están en el JSON
        skill_ids_in_data = [i["id"] for i in skills_data if i.get("id")]
        instance.skills.exclude(id__in=skill_ids_in_data).delete()
        for skill_data in skills_data:
            skill_id = skill_data.get("id")
            if skill_id:
                try:
                    skill = instance.skills.get(id=skill_id)
                    logger.info(
                        f"Actualizando Skill con ID: {skill_id} para el Resume: {instance.id}"
                    )
                    for key, value in skill_data.items():
                        setattr(skill, key, value)
                    skill.save()
                except Skill.DoesNotExist:
                    logger.warning(
                        f"Skill con ID: {skill_id} no encontrado. Creando uno nuevo."
                    )
                    Skill.objects.create(resume=instance, **skill_data)
            else:
                logger.info(f"Creando un nuevo Skill para el Resume: {instance.id}")
                Skill.objects.create(resume=instance, **skill_data)

        experience_ids_in_data = [i["id"] for i in experiences_data if i.get("id")]
        instance.experiences.exclude(id__in=experience_ids_in_data).delete()
        for experience_data in experiences_data:
            experience_id = experience_data.get("id")
            if experience_id:
                try:
                    experience = instance.experiences.get(id=experience_id)
                    logger.info(
                        f"Actualizando Experience con ID: {experience_id} para el Resume: {instance.id}"
                    )
                    for key, value in experience_data.items():
                        setattr(experience, key, value)
                    experience.save()
                except Experience.DoesNotExist:
                    logger.warning(
                        f"Experience con ID: {experience_id} no encontrado. Creando uno nuevo."
                    )
                    Experience.objects.create(resume=instance, **experience_data)
            else:
                logger.info(
                    f"Creando un nuevo Experience para el Resume: {instance.id}"
                )
                Experience.objects.create(resume=instance, **experience_data)

        logger.info(f"Resume actualizado exitosamente: {instance.id}")
        return instance
