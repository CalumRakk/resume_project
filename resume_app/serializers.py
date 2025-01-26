from rest_framework import serializers
from .models import Resume, Skill, Experience, Template


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = ["id", "name", "level", "keywords"]

    def validate(self, data):
        if "resume" not in data:
            return data
        return super().validate(data)


class ExperienceSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Template
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = "__all__"

    def create(self, validated_data):
        skills_data = validated_data.pop("skills", [])
        experiences_data = validated_data.pop("experiences", [])
        resume = Resume.objects.create(**validated_data)

        for experience_data in experiences_data:
            Experience.objects.create(resume=resume, **experience_data)
        for skill_data in skills_data:
            Skill.objects.create(resume=resume, **skill_data)
        return resume

    def update(self, instance, validated_data):
        skills_data = validated_data.pop("skills", [])
        experiences_data = validated_data.pop("experiences", [])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        for skill_data in skills_data:
            skill_id = skill_data.get("id")
            if skill_id:
                skill = instance.skills.get(id=skill_id)
                for key, value in skill_data.items():
                    setattr(skill, key, value)
                skill.save()
            else:
                Skill.objects.create(resume=instance, **skill_data)

        for experience_data in experiences_data:
            experience = instance.experiences.get(id=experience_data.get("id"))
            for key, value in experience_data.items():
                setattr(experience, key, value)
            experience.save()

        return instance
