from rest_framework import serializers
from .models import Resume, Skill, Experience, Template


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    template_selected = TemplateSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = "__all__"
