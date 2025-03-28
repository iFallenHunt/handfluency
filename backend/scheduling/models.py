from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


class TeacherAvailability(models.Model):
    """
    Modelo representando a disponibilidade de horários de um professor.
    """

    WEEKDAY_CHOICES = [
        (0, _("Segunda-feira")),
        (1, _("Terça-feira")),
        (2, _("Quarta-feira")),
        (3, _("Quinta-feira")),
        (4, _("Sexta-feira")),
        (5, _("Sábado")),
        (6, _("Domingo")),
    ]

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availabilities",
        verbose_name=_("professor"),
        limit_choices_to={"user_type": "teacher"},
    )

    weekday = models.PositiveSmallIntegerField(
        _("dia da semana"), choices=WEEKDAY_CHOICES
    )

    start_time = models.TimeField(_("horário de início"))
    end_time = models.TimeField(_("horário de término"))

    is_active = models.BooleanField(_("ativo"), default=True)
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Disponibilidade de Professor")
        verbose_name_plural = _("Disponibilidades de Professores")
        ordering = ["teacher", "weekday", "start_time"]
        unique_together = [["teacher", "weekday", "start_time", "end_time"]]

    def __str__(self) -> str:
        weekday_name = dict(self.WEEKDAY_CHOICES)[self.weekday]
        return (
            f"{self.teacher.get_full_name()} - {weekday_name} "
            f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        )

    def clean(self):
        """
        Validação para garantir que o horário de início seja anterior ao horário de término.
        """
        from django.core.exceptions import ValidationError

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                {
                    "start_time": _(
                        "O horário de início deve ser anterior ao horário de término."
                    )
                }
            )


class ScheduledClass(models.Model):
    """
    Modelo representando uma aula agendada entre aluno e professor.
    """

    STATUS_CHOICES = [
        ("scheduled", _("Agendada")),
        ("confirmed", _("Confirmada")),
        ("completed", _("Concluída")),
        ("cancelled", _("Cancelada")),
        ("missed", _("Perdida")),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scheduled_classes_as_student",
        verbose_name=_("aluno"),
        limit_choices_to={"user_type": "student"},
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scheduled_classes_as_teacher",
        verbose_name=_("professor"),
        limit_choices_to={"user_type": "teacher"},
    )

    date = models.DateField(_("data"))
    start_time = models.TimeField(_("horário de início"))
    end_time = models.TimeField(_("horário de término"))

    status = models.CharField(
        _("status"), max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    topic = models.CharField(
        _("tema"), max_length=200, help_text=_("Tema/assunto a ser trabalhado na aula")
    )

    notes = models.TextField(
        _("observações"),
        blank=True,
        help_text=_("Observações ou requisitos específicos para a aula"),
    )

    meeting_link = models.URLField(
        _("link da reunião"),
        blank=True,
        help_text=_("Link para a sala virtual da aula"),
    )

    feedback = models.TextField(
        _("feedback"), blank=True, help_text=_("Feedback do professor após a aula")
    )

    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Aula Agendada")
        verbose_name_plural = _("Aulas Agendadas")
        ordering = ["date", "start_time"]

    def __str__(self) -> str:
        return (
            f"Aula: {self.student.get_full_name()} com "
            f"{self.teacher.get_full_name()} - {self.date} "
            f"{self.start_time.strftime('%H:%M')}"
        )

    @property
    def is_past(self):
        """Verifica se a aula já passou."""
        now = timezone.now()
        class_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.end_time)
        )
        return now > class_datetime

    def clean(self):
        """
        Validações personalizadas para o agendamento de aulas.
        """
        from django.core.exceptions import ValidationError

        # Horário de início deve ser anterior ao horário de término
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                {
                    "start_time": _(
                        "O horário de início deve ser anterior ao horário de término."
                    )
                }
            )

        # Aula não pode ser agendada no passado
        if self.date and self.date < timezone.now().date():
            raise ValidationError(
                {"date": _("Não é possível agendar aulas para datas passadas.")}
            )


class ClassNotification(models.Model):
    """
    Modelo para notificações relacionadas a aulas agendadas.
    """

    TYPE_CHOICES = [
        ("scheduled", _("Aula Agendada")),
        ("reminder", _("Lembrete de Aula")),
        ("cancellation", _("Cancelamento")),
        ("rescheduled", _("Reagendamento")),
    ]

    scheduled_class = models.ForeignKey(
        ScheduledClass,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("aula agendada"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="class_notifications",
        verbose_name=_("destinatário"),
    )

    notification_type = models.CharField(
        _("tipo de notificação"), max_length=20, choices=TYPE_CHOICES
    )

    message = models.TextField(_("mensagem"))

    sent_at = models.DateTimeField(_("enviado em"), auto_now_add=True)
    read = models.BooleanField(_("lido"), default=False)
    read_at = models.DateTimeField(_("lido em"), null=True, blank=True)

    class Meta:
        verbose_name = _("Notificação de Aula")
        verbose_name_plural = _("Notificações de Aulas")
        ordering = ["-sent_at"]

    def __str__(self) -> str:
        return (
            f"{self.get_notification_type_display()} - {self.recipient.get_full_name()}"
        )

    def mark_as_read(self):
        """Marca a notificação como lida."""
        if not self.read:
            self.read = True
            self.read_at = timezone.now()
            self.save(update_fields=["read", "read_at"])
