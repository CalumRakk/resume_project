from rest_framework import serializers
from .models import Resume, Skill, Experience, Template


class SkillSerializer(serializers.ModelSerializer):
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
