"""
Modelos para o app users, definindo estruturas de dados para usuários.
Otimizado para uso com Supabase como banco de dados.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from typing import Optional

from core.base_models import SupabaseBaseModel, RelatedObjectCache


class User(SupabaseBaseModel, AbstractUser):
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
    profile_picture = models.URLField(
        _("URL da foto de perfil"), 
        blank=True, 
        max_length=500,
        help_text=_("URL para imagem de perfil no bucket do Supabase")
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
    
    # Flag para preferências de notificação
    email_notifications = models.BooleanField(
        _("notificações por email"), 
        default=True,
        help_text=_("Receber notificações por email")
    )

    def is_student(self) -> bool:
        """Verifica se o usuário é um aluno."""
        return self.user_type == self.UserType.STUDENT

    def is_teacher(self) -> bool:
        """Verifica se o usuário é um professor."""
        return self.user_type == self.UserType.TEACHER

    def is_admin(self) -> bool:
        """Verifica se o usuário é um administrador."""
        return self.user_type == self.UserType.ADMIN

    def __str__(self) -> str:
        """Representação em string do usuário."""
        if self.get_full_name():
            return self.get_full_name()
        return str(self.username)

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        db_table = "users"
        indexes = [
            models.Index(fields=["email"], name="idx_user_email"),
            models.Index(fields=["user_type"], name="idx_user_type"),
            models.Index(fields=["username"], name="idx_username")
        ]


class UserProfile(SupabaseBaseModel):
    """
    Perfil adicional do usuário, armazenando informações complementares.
    """

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile",
        help_text=_("Usuário ao qual este perfil pertence")
    )

    # Informações de contato adicionais
    phone_number = models.CharField(_("número de telefone"), max_length=20, blank=True)
    alternative_email = models.EmailField(_("email alternativo"), blank=True)
    
    # Informações de perfil
    birth_date = models.DateField(_("data de nascimento"), null=True, blank=True)
    city = models.CharField(_("cidade"), max_length=100, blank=True)
    state = models.CharField(_("estado"), max_length=50, blank=True)
    country = models.CharField(_("país"), max_length=100, blank=True, default="Brasil")

    # Preferências do usuário (armazenadas como JSON)
    notification_preferences = models.JSONField(
        _("preferências de notificação"), 
        default=dict, 
        blank=True,
        help_text=_("Configurações detalhadas de notificações")
    )

    # Horários disponíveis (apenas para professores)
    available_hours = models.JSONField(
        _("horários disponíveis"), 
        default=dict, 
        blank=True,
        help_text=_("Horários em que o professor está disponível")
    )
    
    # Campos para caching
    _user_cache: Optional[RelatedObjectCache[User]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_cache = RelatedObjectCache(User)

    def __str__(self) -> str:
        """Representação em string do perfil de usuário."""
        user = self._user_cache.get(self, "user")
        if user:
            if user.get_full_name():
                return f"Perfil de {user.get_full_name()}"
            return f"Perfil de {user.username}"
        return f"Perfil {self.id}"

    def clean(self):
        """Validações personalizadas para o perfil."""
        from django.core.exceptions import ValidationError
        
        # Validação de data de nascimento (não pode ser no futuro)
        from django.utils import timezone
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({
                "birth_date": _("A data de nascimento não pode ser no futuro.")
            })

    class Meta:
        verbose_name = _("Perfil de Usuário")
        verbose_name_plural = _("Perfis de Usuários")
        db_table = "user_profiles"
        indexes = [
            models.Index(fields=["user"], name="idx_profile_user"),
            models.Index(fields=["phone_number"], name="idx_phone_number")
        ]
