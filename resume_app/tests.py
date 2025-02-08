from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework.exceptions import ErrorDetail

from .models import Resume, Skill, Experience, Template
from .serializers import (
    ResumeSerializer,
    SkillSerializer,
    ExperienceSerializer,
    TemplateSerializer,
)

### Models Tests ###


class ResumeModelTest(TestCase):
    """
    Pruebas para el modelo Resume.
    """

    def setUp(self):
        """
        Configuración inicial para las pruebas del modelo Resume.
        Crea un usuario y una plantilla para ser utilizados en las pruebas.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.template = Template.objects.create(
            name="Modern",
            descripcion="Plantilla moderna",
            componet_name="modern-resume",
        )

    def test_resume_creation(self):
        """
        Verifica la creación exitosa de un objeto Resume con todos los campos obligatorios.
        """
        resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="Desarrollador web con experiencia...",
            template_selected=self.template,
            user=self.user,
        )
        self.assertEqual(resume.full_name, "John Doe")
        self.assertEqual(resume.email, "john.doe@example.com")
        self.assertEqual(
            str(resume), f"[Resume] {resume.id}"
        )  # Prueba del método __str__
        self.assertIsNotNone(resume.created_at)
        self.assertIsNotNone(resume.updated_at)

    def test_resume_blank_fields(self):
        """
        Verifica que el campo 'summary' puede estar vacío al crear un Resume.
        """
        resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="",
            template_selected=self.template,
            user=self.user,
        )  # Summary puede estar vacio
        self.assertEqual(resume.summary, "")

    def test_resume_missing_fields(self):
        """
        Verifica que los campos obligatorios (full_name, email) no puedan estar vacíos.
        Espera una excepción ValidationError si faltan campos obligatorios.
        """
        with self.assertRaises(ValidationError):
            Resume.objects.create(
                full_name="",
                email="",
                summary="Desarrollador web con experiencia...",
                template_selected=self.template,
                user=self.user,
            ).full_clean()

    def test_resume_email_validation(self):
        """
        Verifica que el campo 'email' tenga un formato válido.
        Espera una excepción ValidationError si el formato del email no es válido.
        """
        with self.assertRaises(ValidationError):
            resume = Resume(
                full_name="John Doe",
                email="invalid-email",
                summary="Desarrollador web con experiencia...",
                template_selected=self.template,
                user=self.user,
            )
            resume.full_clean()

    def test_resume_template_relation(self):
        """
        Verifica la relación ForeignKey entre Resume y Template.
        Asegura que el campo template_selected esté correctamente relacionado.
        """
        resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="Desarrollador web con experiencia...",
            template_selected=self.template,
            user=self.user,
        )
        self.assertEqual(resume.template_selected, self.template)
        self.assertEqual(self.template.resumes.count(), 1)

    def test_resume_user_relation(self):
        """
        Verifica la relación ForeignKey entre Resume y User.
        Asegura que el campo user esté correctamente relacionado.
        """
        resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="Desarrollador web con experiencia...",
            template_selected=self.template,
            user=self.user,
        )
        self.assertEqual(resume.user, self.user)
        self.assertEqual(self.user.resumes.count(), 1)


class SkillModelTest(TestCase):
    """
    Pruebas para el modelo Skill.
    """

    def setUp(self):
        """
        Configuración inicial para las pruebas del modelo Skill.
        Crea un usuario y un Resume para ser utilizados en las pruebas.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="Desarrollador web con experiencia...",
            user=self.user,
        )

    def test_skill_creation(self):
        """
        Verifica la creación exitosa de un objeto Skill con todos los campos obligatorios.
        """
        skill = Skill.objects.create(
            name="Python", resume=self.resume, level="Avanzado", orden=0
        )
        self.assertEqual(skill.name, "Python")
        self.assertEqual(skill.level, "Avanzado")
        self.assertEqual(skill.resume, self.resume)
        self.assertEqual(skill.orden, 0)
        self.assertEqual(str(skill), f"[Skill] {skill.id}")  # Prueba del método __str__
        self.assertIsNotNone(skill.created_at)
        self.assertIsNotNone(skill.updated_at)

    def test_skill_default_values(self):
        """
        Verifica que los valores por defecto para los campos name y level se asignen correctamente.
        """
        skill = Skill.objects.create(resume=self.resume, orden=0)
        self.assertEqual(skill.name, "Web Development")
        self.assertEqual(skill.level, "Master")

    def test_skill_unique_order_per_resume(self):
        """
        Verifica la restricción de unicidad del campo 'orden' por cada Resume.
        Espera una excepción IntegrityError si se intenta crear dos Skill con el mismo orden para el mismo Resume.
        """
        Skill.objects.create(
            name="Python", resume=self.resume, level="Avanzado", orden=0
        )
        with self.assertRaises(IntegrityError):
            Skill.objects.create(
                name="JavaScript", resume=self.resume, level="Intermedio", orden=0
            )

    def test_skill_resume_relation(self):
        """
        Verifica la relación ForeignKey entre Skill y Resume.
        Asegura que el campo resume esté correctamente relacionado.
        """
        skill = Skill.objects.create(
            name="Python", resume=self.resume, level="Avanzado", orden=0
        )
        self.assertEqual(skill.resume, self.resume)
        self.assertEqual(self.resume.skills.count(), 1)


class ExperienceModelTest(TestCase):
    """
    Pruebas para el modelo Experience.
    """

    def setUp(self):
        """
        Configuración inicial para las pruebas del modelo Experience.
        Crea un usuario y un Resume para ser utilizados en las pruebas.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.resume = Resume.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            summary="Desarrollador web con experiencia...",
            user=self.user,
        )

    def test_experience_creation(self):
        """
        Verifica la creación exitosa de un objeto Experience con todos los campos obligatorios.
        """
        experience = Experience.objects.create(
            name="Empresa XYZ",
            position="Desarrollador Frontend",
            url="https://www.empresa.com",
            summary="Desarrollé interfaces de usuario...",
            start_date="2023-01-01",
            end_date="2024-01-01",
            resume=self.resume,
            orden=0,
        )
        self.assertEqual(experience.name, "Empresa XYZ")
        self.assertEqual(experience.position, "Desarrollador Frontend")
        self.assertEqual(experience.url, "https://www.empresa.com")
        self.assertEqual(
            str(experience), f"[Experience] {experience.id}"
        )  # Prueba del método __str__
        self.assertIsNotNone(experience.created_at)
        self.assertIsNotNone(experience.updated_at)

    def test_experience_default_values(self):
        """
        Verifica que los valores por defecto para los campos name, position y url se asignen correctamente.
        """
        experience = Experience.objects.create(resume=self.resume, orden=0)
        self.assertEqual(experience.name, "Company Name")
        self.assertEqual(experience.position, "President")
        self.assertEqual(experience.url, "https://company.com")

    def test_experience_unique_order_per_resume(self):
        """
        Verifica la restricción de unicidad del campo 'orden' por cada Resume.
        Espera una excepción IntegrityError si se intenta crear dos Experience con el mismo orden para el mismo Resume.
        """
        Experience.objects.create(
            name="Empresa XYZ",
            position="Desarrollador Frontend",
            url="https://www.empresa.com",
            summary="Desarrollé interfaces de usuario...",
            start_date="2023-01-01",
            end_date="2024-01-01",
            resume=self.resume,
            orden=0,
        )
        with self.assertRaises(IntegrityError):
            Experience.objects.create(
                name="Otra empresa",
                position="Desarrollador Backend",
                url="https://www.otraempresa.com",
                summary="Desarrollé APIs...",
                start_date="2022-01-01",
                end_date="2023-01-01",
                resume=self.resume,
                orden=0,
            )

    def test_experience_resume_relation(self):
        """
        Verifica la relación ForeignKey entre Experience y Resume.
        Asegura que el campo resume esté correctamente relacionado.
        """
        experience = Experience.objects.create(
            name="Empresa XYZ",
            position="Desarrollador Frontend",
            url="https://www.empresa.com",
            summary="Desarrollé interfaces de usuario...",
            start_date="2023-01-01",
            end_date="2024-01-01",
            resume=self.resume,
            orden=0,
        )
        self.assertEqual(experience.resume, self.resume)
        self.assertEqual(self.resume.experiences.count(), 1)


class TemplateModelTest(TestCase):
    """
    Pruebas para el modelo Template.
    """

    def test_template_creation(self):
        """
        Verifica la creación exitosa de un objeto Template con todos los campos obligatorios.
        """
        template = Template.objects.create(
            name="Modern",
            descripcion="Plantilla moderna",
            componet_name="modern-resume",
        )
        self.assertEqual(template.name, "Modern")
        self.assertEqual(template.descripcion, "Plantilla moderna")
        self.assertEqual(template.componet_name, "modern-resume")
        self.assertEqual(str(template), f"[Template] {template.id}")
        self.assertIsNotNone(template.created_at)
        self.assertIsNotNone(template.updated_at)

    def test_template_customazation_rules_default(self):
        """
        Verifica que el campo 'customazation_rules' tenga el valor por defecto (lista vacía).
        """
        template = Template.objects.create(
            name="Modern",
            descripcion="Plantilla moderna",
            componet_name="modern-resume",
        )
        self.assertEqual(template.customazation_rules, [])


### Serializers Test ###


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
                "customazation_rules": self.template.customazation_rules,
            },
            "skills": [],
            "experiences": [],
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
        self.assertEqual(
            serializer.errors["email"][0],
            ErrorDetail(string="Ingrese un correo electrónico válido.", code="invalid"),
        )

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
        self.assertTrue(serializer.is_valid())
        serializer.save()

        resume.refresh_from_db()  # Refresca el objeto desde la base de datos
        self.assertEqual(resume.full_name, "Updated Name")
        self.assertEqual(resume.email, "updated@example.com")
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
                {"name": "Python", "level": "Avanzado", "orden": 0},
                {"name": "Django", "level": "Experto", "orden": 1},
            ],
            "experiences": [
                {
                    "name": "Empresa ABC",
                    "position": "Desarrolladora Backend",
                    "url": "https://www.empresaabc.com",
                    "summary": "Desarrollé APIs...",
                    "start_date": "2022-01-01",
                    "end_date": "2023-01-01",
                    "orden": 0,
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
            name="Python", resume=self.resume, level="Avanzado", orden=0
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
            "orden": skill.orden,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_skill_serializer_create(self):
        """
        Verifica que el serializador SkillSerializer crea correctamente un nuevo objeto Skill.
        """
        data = {"name": "JavaScript", "level": "Intermedio", "orden": 1}
        serializer = SkillSerializer(data=data, context={"resume": self.resume})
        serializer.resume = self.resume
        self.assertTrue(serializer.is_valid())
        skill = serializer.save(resume=self.resume)
        self.assertEqual(skill.name, "JavaScript")
        self.assertEqual(skill.level, "Intermedio")
        self.assertEqual(skill.resume, self.resume)
        self.assertEqual(skill.orden, 1)

    def test_skill_serializer_update(self):
        """
        Verifica que el serializador SkillSerializer actualiza correctamente un objeto Skill existente.
        """
        skill = self.skill
        data = {"name": "Updated Skill", "level": "Updated Level", "orden": 2}
        serializer = SkillSerializer(skill, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        skill.refresh_from_db()
        self.assertEqual(skill.name, "Updated Skill")
        self.assertEqual(skill.level, "Updated Level")
        self.assertEqual(skill.orden, 2)


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
            orden=0,
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
            "orden": experience.orden,
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
            "orden": 1,
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
        self.assertEqual(experience.orden, 1)

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
            "orden": 2,
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
        self.assertEqual(experience.orden, 2)


class TemplateSerializerTest(SerializerTestSetUp):
    def setUp(self):
        super().setUp()
        self.template = Template.objects.create(
            name="Basic", descripcion="Plantilla básica", componet_name="basic-resume"
        )

    def test_template_serializer_valid(self):
        """
        Verifica que el serializador TemplateSerializer serializa correctamente un objeto Template.
        """
        template = self.template
        serializer = TemplateSerializer(template)
        expected_data = {
            "id": template.id,
            "name": template.name,
            "descripcion": template.descripcion,
            "componet_name": template.componet_name,
            "customazation_rules": template.customazation_rules,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_template_serializer_create(self):
        """
        Verifica que el serializador TemplateSerializer crea correctamente un nuevo objeto Template.
        """
        data = {
            "name": "New Template",
            "descripcion": "Descripción de la nueva plantilla",
            "componet_name": "new-template",
            "customazation_rules": [],
        }
        serializer = TemplateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        template = serializer.save()
        self.assertEqual(template.name, "New Template")
        self.assertEqual(template.descripcion, "Descripción de la nueva plantilla")
        self.assertEqual(template.componet_name, "new-template")
        self.assertEqual(template.customazation_rules, [])

    def test_template_serializer_update(self):
        """
        Verifica que el serializador TemplateSerializer actualiza correctamente un objeto Template existente.
        """
        template = self.template
        data = {
            "name": "Updated Template",
            "descripcion": "Updated descripción",
            "componet_name": "updated-template",
            "customazation_rules": ["rule1", "rule2"],
        }
        serializer = TemplateSerializer(template, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        template.refresh_from_db()
        self.assertEqual(template.name, "Updated Template")
        self.assertEqual(template.descripcion, "Updated descripción")
        self.assertEqual(template.componet_name, "updated-template")
        self.assertEqual(template.customazation_rules, ["rule1", "rule2"])
