from django.contrib import admin
from .models import Resume, Skill, Experience, Template


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "template_selected",
    )
    list_filter = ("template_selected",)
    search_fields = ("full_name", "email")
    inlines = [
        SkillInline,
        ExperienceInline,
    ]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "componet_name")


admin.site.register(Skill)
admin.site.register(Experience)
