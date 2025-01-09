from rest_framework import serializers
from .models import Resume, Skill, Experience, Template, ResumeCustomization


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
    # resume = serializers.HyperlinkedRelatedField(
    #     view_name="resume-detail",
    #     lookup_field="pk",
    #     queryset=Resume.objects.all(),
    #     required=False,
    #     allow_null=True,
    # )

    class Meta:
        model = Template
        fields = [
            "id",
            "url",
            "name",
            "descripcion",
            "componet_name",
            "customazation_rules",
            # "resume",
        ]


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
    template_selected = serializers.PrimaryKeyRelatedField(
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
            "template_selected",
        ]


class SkillSerializer(serializers.ModelSerializer):
    resume = serializers.HyperlinkedRelatedField(
        view_name="resume-detail", lookup_field="pk", queryset=Resume.objects.all()
    )

    class Meta:
        model = Skill
        fields = ["id", "url", "name", "level", "keywords", "resume"]


class ResumeCustomizationSerializer(serializers.ModelSerializer):
    resume = serializers.HyperlinkedRelatedField(
        view_name="resume-detail", lookup_field="pk", queryset=Resume.objects.all()
    )
    template = serializers.HyperlinkedRelatedField(
        view_name="template-detail", lookup_field="pk", queryset=Template.objects.all()
    )

    class Meta:
        model = ResumeCustomization
        fields = [
            "id",
            "url",
            "resume",
            "template",
            "custom_styles",
        ]
