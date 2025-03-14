from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework.exceptions import ErrorDetail

from resume_app.models import Resume, Skill, Experience, Template
from resume_app.serializers import (
    ResumeSerializer,
    SkillSerializer,
    ExperienceSerializer,
    TemplateSerializer,
)


class SerializerTestSetUp(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.template = Template.objects.create(
            name="Modern",
            descripcion="Plantilla moderna",
            componet_name="modern-resume",
            user=self.user
        )
        self.resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="Desarrollador web con experiencia...",
            template_selected=self.template,
            user=self.user,
        )


class ResumeSerializerTest(SerializerTestSetUp):
    def test_resume_serializer_valid(self):
        """
        Verifica que el serializador ResumeSerializer serializa correctamente un objeto Resume.
        """
        resume = self.resume
        serializer = ResumeSerializer(resume)
        expected_data = {
            "id": resume.id,
            "full_name": resume.full_name,
            "email": resume.email,
            "created_at": resume.created_at.isoformat().replace("+00:00", "Z"),
            "updated_at": resume.updated_at.isoformat().replace("+00:00", "Z"),
            "summary": resume.summary,
            "template_selected": {
                "id": self.template.id,
                "name": self.template.name,
                "descripcion": self.template.descripcion,
                "componet_name": self.template.componet_name,
                "customization_rules": self.template.customization_rules,
            },
            "skills": [],
            "experiences": [],
            "customization": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_resume_serializer_invalid_email(self):
        """
        Verifica que el serializador ResumeSerializer valida correctamente el formato del email.
        """
        data = {
            "full_name": "John Doe",
            "email": "invalid-email",
            "summary": "Desarrollador web con experiencia...",
            "template_selected": self.template.id,
        }
        request = self.factory.get("/")
        request.user = self.user
        serializer = ResumeSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIsInstance(serializer.errors["email"][0], ErrorDetail)

    def test_resume_serializer_create(self):
        """
        Verifica que el serializador ResumeSerializer crea correctamente un nuevo objeto Resume.
        """
        data = {
            "full_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "summary": "Desarrolladora web con experiencia...",
            "template_selected": self.template.id,
        }
        request = self.factory.get("/")
        request.user = self.user
        serializer = ResumeSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid())
        resume = serializer.save()
        self.assertEqual(resume.full_name, "Jane Doe")
        self.assertEqual(resume.email, "jane.doe@example.com")
        self.assertEqual(resume.summary, "Desarrolladora web con experiencia...")
        self.assertEqual(resume.template_selected, self.template)
        self.assertEqual(resume.user, self.user)

    def test_resume_serializer_update(self):
        """
        Verifica que el serializador ResumeSerializer actualiza correctamente un objeto Resume existente.
        """
        resume = self.resume
        data = {
            "full_name": "Updated Name",
            "email": "updated@example.com",
            "summary": "Updated summary",
            "template_selected": self.template.id,
        }

        request = self.factory.get("/")
        request.user = self.user
        serializer = ResumeSerializer(resume, data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), msg="Serializer no es valido")
        serializer.save()

        resume.refresh_from_db()  # Refresca el objeto desde la base de datos
        self.assertEqual(
            resume.full_name, "Updated Name", msg="full_name no actualizado"
        )
        self.assertEqual(
            resume.email, "updated@example.com", msg="Email no actualizado"
        )
        self.assertEqual(resume.summary, "Updated summary")
        self.assertEqual(resume.template_selected, self.template)

    def test_resume_serializer_create_with_skills_and_experiences(self):
        """
        Verifica que el serializador ResumeSerializer crea correctamente un nuevo objeto Resume con skills y experiences.
        """
        data = {
            "full_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "summary": "Desarrolladora web con experiencia...",
            "template_selected": self.template.id,
            "skills": [
                {"name": "Python", "level": "Avanzado"},
                {"name": "Django", "level": "Experto"},
            ],
            "experiences": [
                {
                    "name": "Empresa ABC",
                    "position": "Desarrolladora Backend",
                    "url": "https://www.empresaabc.com",
                    "summary": "Desarrollé APIs...",
                    "start_date": "2022-01-01",
                    "end_date": "2023-01-01",
                }
            ],
        }
        request = self.factory.get("/")
        request.user = self.user
        serializer = ResumeSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid())
        resume = serializer.save()
        self.assertEqual(resume.skills.count(), 2)
        self.assertEqual(resume.experiences.count(), 1)


class SkillSerializerTest(SerializerTestSetUp):
    def setUp(self):
        super().setUp()
        self.skill = Skill.objects.create(
            name="Python", resume=self.resume, level="Avanzado"
        )

    def test_skill_serializer_valid(self):
        """
        Verifica que el serializador SkillSerializer serializa correctamente un objeto Skill.
        """
        skill = self.skill
        serializer = SkillSerializer(skill)
        expected_data = {
            "id": skill.id,
            "name": skill.name,
            "level": skill.level,
            "keywords": skill.keywords,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_skill_serializer_create(self):
        """
        Verifica que el serializador SkillSerializer crea correctamente un nuevo objeto Skill.
        """
        data = {"name": "JavaScript", "level": "Intermedio"}
        serializer = SkillSerializer(data=data, context={"resume": self.resume})
        serializer.resume = self.resume
        self.assertTrue(serializer.is_valid())
        skill = serializer.save(resume=self.resume)
        self.assertEqual(skill.name, "JavaScript")
        self.assertEqual(skill.level, "Intermedio")
        self.assertEqual(skill.resume, self.resume)

    def test_skill_serializer_update(self):
        """
        Verifica que el serializador SkillSerializer actualiza correctamente un objeto Skill existente.
        """
        skill = self.skill
        data = {"name": "Updated Skill", "level": "Updated Level"}
        serializer = SkillSerializer(skill, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        skill.refresh_from_db()
        self.assertEqual(skill.name, "Updated Skill")
        self.assertEqual(skill.level, "Updated Level")


class ExperienceSerializerTest(SerializerTestSetUp):
    def setUp(self):
        super().setUp()
        self.experience = Experience.objects.create(
            name="Empresa XYZ",
            position="Desarrollador Frontend",
            url="https://www.empresa.com",
            summary="Desarrollé interfaces de usuario...",
            start_date="2022-01-01",
            end_date="2022-01-01",
            resume=self.resume,
        )

    def test_experience_serializer_valid(self):
        """
        Verifica que el serializador ExperienceSerializer serializa correctamente un objeto Experience.
        """
        experience = self.experience
        serializer = ExperienceSerializer(experience)
        expected_data = {
            "id": experience.id,
            "name": experience.name,
            "position": experience.position,
            "url": experience.url,
            "highlights": experience.highlights,
            "summary": experience.summary,
            "start_date": experience.start_date,
            "end_date": experience.end_date,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_experience_serializer_create(self):
        """
        Verifica que el serializador ExperienceSerializer crea correctamente un nuevo objeto Experience.
        """
        data = {
            "name": "Nueva Empresa",
            "position": "Desarrollador Backend",
            "url": "https://www.nuevaempresa.com",
            "summary": "Desarrollé APIs...",
            "start_date": "2022-01-01",
            "end_date": "2022-01-01",
        }
        serializer = ExperienceSerializer(data=data, context={"resume": self.resume})
        serializer.resume = self.resume

        self.assertTrue(serializer.is_valid())
        experience = serializer.save(resume=self.resume)
        self.assertEqual(experience.name, "Nueva Empresa")
        self.assertEqual(experience.position, "Desarrollador Backend")
        self.assertEqual(experience.url, "https://www.nuevaempresa.com")
        self.assertEqual(experience.summary, "Desarrollé APIs...")
        self.assertEqual(experience.start_date.isoformat(), "2022-01-01")
        self.assertEqual(experience.end_date.isoformat(), "2022-01-01")
        self.assertEqual(experience.resume, self.resume)

    def test_experience_serializer_update(self):
        """
        Verifica que el serializador ExperienceSerializer actualiza correctamente un objeto Experience existente.
        """
        experience = self.experience
        data = {
            "name": "Updated Empresa",
            "position": "Updated Position",
            "url": "https://www.updated.com",
            "summary": "Updated summary",
            "start_date": "2021-01-01",
            "end_date": "2022-01-01",
        }
        serializer = ExperienceSerializer(experience, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        experience.refresh_from_db()
        self.assertEqual(experience.name, "Updated Empresa")
        self.assertEqual(experience.position, "Updated Position")
        self.assertEqual(experience.url, "https://www.updated.com")
        self.assertEqual(experience.summary, "Updated summary")
        self.assertEqual(experience.start_date.isoformat(), "2021-01-01")
        self.assertEqual(experience.end_date.isoformat(), "2022-01-01")


# class TemplateSerializerTest(SerializerTestSetUp):
#     def setUp(self):
#         super().setUp()
#         self.template = Template.objects.create(
#             name="Basic", descripcion="Plantilla básica", componet_name="basic-resume"
#         )

#     def test_template_serializer_valid(self):
#         """
#         Verifica que el serializador TemplateSerializer serializa correctamente un objeto Template.
#         """
#         template = self.template
#         serializer = TemplateSerializer(template)
#         expected_data = {
#             "id": template.id,
#             "name": template.name,
#             "descripcion": template.descripcion,
#             "componet_name": template.componet_name,
#             "customization_rules": template.customization_rules,
#         }
#         self.assertEqual(serializer.data, expected_data)

#     def test_template_serializer_create(self):
#         """
#         Verifica que el serializador TemplateSerializer crea correctamente un nuevo objeto Template.
#         """
#         data = {
#             "name": "New Template",
#             "descripcion": "Descripción de la nueva plantilla",
#             "componet_name": "new-template",
#             "customization_rules": [],
#         }
#         serializer = TemplateSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         template = serializer.save()
#         self.assertEqual(template.name, "New Template")
#         self.assertEqual(template.descripcion, "Descripción de la nueva plantilla")
#         self.assertEqual(template.componet_name, "new-template")
#         self.assertEqual(template.customization_rules, [])

#     def test_template_serializer_update(self):
#         """
#         Verifica que el serializador TemplateSerializer actualiza correctamente un objeto Template existente.
#         """
#         template = self.template
#         data = {
#             "name": "Updated Template",
#             "descripcion": "Updated descripción",
#             "componet_name": "updated-template",
#             "customization_rules": ["rule1", "rule2"],
#         }
#         serializer = TemplateSerializer(template, data=data)
#         self.assertTrue(serializer.is_valid())
#         serializer.save()
#         template.refresh_from_db()
#         self.assertEqual(template.name, "Updated Template")
#         self.assertEqual(template.descripcion, "Updated descripción")
#         self.assertEqual(template.componet_name, "updated-template")
#         self.assertEqual(template.customization_rules, ["rule1", "rule2"])
