from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User

from .models import Resume, Skill, Experience, Template


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
