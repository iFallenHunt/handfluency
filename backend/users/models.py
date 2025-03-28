from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    """
    Modelo de usuário customizado para a plataforma de ensino de Libras.
    Estende o modelo AbstractUser do Django, adicionando campos específicos.
    """

    class UserType(models.TextChoices):
        STUDENT = "student", _("Aluno")
        TEACHER = "teacher", _("Professor")
        ADMIN = "admin", _("Administrador")

    user_type = models.CharField(
        _("tipo de usuário"),
        max_length=10,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )

    bio = models.TextField(_("biografia"), blank=True)
    profile_picture = models.ImageField(
        _("foto de perfil"), upload_to="profile_pictures/", blank=True, null=True
    )

    # Campos específicos para professores
    specializations = models.CharField(_("especializações"), max_length=255, blank=True)
    teaching_experience = models.PositiveIntegerField(
        _("anos de experiência"), default=0
    )

    # Campos específicos para alunos
    level = models.CharField(_("nível"), max_length=50, blank=True)

    # Campos para autenticação social
    google_id = models.CharField(
        _("ID do Google"), max_length=100, blank=True, null=True, unique=True
    )

    def is_student(self):
        return self.user_type == self.UserType.STUDENT

    def is_teacher(self):
        return self.user_type == self.UserType.TEACHER

    def is_admin(self):
        return self.user_type == self.UserType.ADMIN

    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        db_table = "users"


class UserProfile(BaseModel):
    """
    Perfil adicional do usuário, armazenando informações complementares.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Informações de contato adicionais
    phone_number = models.CharField(_("número de telefone"), max_length=20, blank=True)

    # Preferências do usuário
    notification_preferences = models.JSONField(
        _("preferências de notificação"), default=dict, blank=True
    )

    # Horários disponíveis (apenas para professores)
    available_hours = models.JSONField(
        _("horários disponíveis"), default=dict, blank=True
    )

    # Dados para relatórios
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if hasattr(self.user, "username") and self.user.username:
            return f"Perfil de {self.user.username}"
        return f"Perfil de usuário {self.id}"

    class Meta:
        verbose_name = _("Perfil de Usuário")
        verbose_name_plural = _("Perfis de Usuários")
        db_table = "user_profiles"
