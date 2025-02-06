from rest_framework import serializers
from .models import Resume, Skill, Experience, Template


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = ["id", "name", "level", "keywords", "orden"]

    def validate(self, data):
        if "resume" not in data:
            return data
        return super().validate(data)


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

    def validate(self, data):
        if "resume" not in data:
            return data
        return super().validate(data)


class TemplateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Template
        fields = ["id", "name", "descripcion", "componet_name", "customazation_rules"]

    def validate(self, attrs):
        return super().validate(attrs)


class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    template_selected = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), required=False, write_only=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Resume
        fields = "__all__"

    def to_representation(self, instance):
        """
        Sobrescribe la representación para incluir el template_selected como un objeto JSON.
        """
        representation = super().to_representation(instance)
        if instance.template_selected:
            representation["template_selected"] = TemplateSerializer(
                instance.template_selected
            ).data
        return representation

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        skills_data = validated_data.pop("skills", [])
        experiences_data = validated_data.pop("experiences", [])
        resume = Resume.objects.create(**validated_data)

        for experience_data in experiences_data:
            Experience.objects.create(resume=resume, **experience_data)
        for skill_data in skills_data:
            Skill.objects.create(resume=resume, **skill_data)
        return resume

    def update(self, instance, validated_data):
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
                    for key, value in skill_data.items():
                        setattr(skill, key, value)
                    skill.save()
                except Skill.DoesNotExist:
                    Skill.objects.create(resume=instance, **skill_data)
            else:
                Skill.objects.create(resume=instance, **skill_data)

        experience_ids_in_data = [i["id"] for i in experiences_data if i.get("id")]
        instance.experiences.exclude(id__in=experience_ids_in_data).delete()
        for experience_data in experiences_data:
            experience_id = experience_data.get("id")
            if experience_id:
                try:
                    experience = instance.experiences.get(id=experience_id)
                    for key, value in experience_data.items():
                        setattr(experience, key, value)
                    experience.save()
                except Experience.DoesNotExist:
                    Experience.objects.create(resume=instance, **experience_data)
            else:
                Experience.objects.create(resume=instance, **experience_data)

        return instance
