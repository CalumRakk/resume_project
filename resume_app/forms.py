from django import forms
from .models import Resume, Skill, Experience
from django.forms.models import inlineformset_factory


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            "full_name",
            "email",
            "summary",
        ]


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "level"]


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["name", "position", "url", "start_date", "end_date"]


SkillFormSet = inlineformset_factory(
    Resume, Skill, form=SkillForm, extra=3, can_delete=True
)

ExperienceFormSet = inlineformset_factory(
    Resume, Experience, form=ExperienceForm, extra=3, can_delete=True
)
