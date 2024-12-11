from rest_framework import serializers
from .models import Resume, Skill, Experience, Template


class ExperienceSerializer(serializers.ModelSerializer):
    resume = serializers.HyperlinkedRelatedField(
        view_name="resume-detail", lookup_field="pk", queryset=Resume.objects.all()
    )

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
            "resume",
        ]
        excludes = ["url"]


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ["name", "html_structure", "styles"]


class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.HyperlinkedRelatedField(
        view_name="skill-detail",
        lookup_field="pk",
        many=True,
        queryset=Skill.objects.all(),
    )
    experiences = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Experience.objects.all(),
        view_name="experience-detail",
        lookup_field="pk",
    )
    template = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), required=False
    )

    class Meta:
        model = Resume
        fields = [
            "id",
            "url",
            "full_name",
            "email",
            "summary",
            "skills",
            "experiences",
            "template",
        ]


class SkillSerializer(serializers.ModelSerializer):
    resume = serializers.HyperlinkedRelatedField(
        view_name="resume-detail", lookup_field="pk", queryset=Resume.objects.all()
    )

    class Meta:
        model = Skill
        fields = ["id", "url", "name", "level", "keywords", "resume"]
