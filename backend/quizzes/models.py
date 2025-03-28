from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from courses.models import Lesson, Course


class Quiz(models.Model):
    """
    Modelo representando um quiz/teste que contém questões.
    """

    title = models.CharField(_("título"), max_length=200)
    description = models.TextField(_("descrição"))

    # Relacionamentos
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name=_("curso"),
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        related_name="quizzes",
        verbose_name=_("aula"),
        null=True,
        blank=True,
    )

    # Configurações
    is_active = models.BooleanField(_("ativo"), default=True)
    time_limit = models.PositiveIntegerField(
        _("limite de tempo (minutos)"),
        help_text=_("Tempo máximo em minutos para completar o quiz"),
        default=0,  # 0 significa sem limite
    )
    passing_score = models.PositiveSmallIntegerField(
        _("nota para aprovação (%)"),
        default=70,
        help_text=_("Pontuação mínima percentual para passar no quiz"),
    )

    # Metadados
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes_created",
        verbose_name=_("criado por"),
    )

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    @property
    def total_questions(self):
        return self.questions.count()

    @property
    def max_score(self):
        return sum(question.points for question in self.questions.all())


class Question(models.Model):
    """
    Modelo representando uma pergunta em um quiz.
    """

    TYPE_CHOICES = [
        ("multiple_choice", _("Múltipla Escolha")),
        ("true_false", _("Verdadeiro/Falso")),
        ("matching", _("Associação")),
        ("ordering", _("Ordenação")),
        ("fill_in", _("Preencher Lacunas")),
        ("video_response", _("Resposta em Vídeo")),
    ]

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name=_("quiz")
    )

    text = models.TextField(_("texto da pergunta"))
    question_type = models.CharField(
        _("tipo de questão"),
        max_length=20,
        choices=TYPE_CHOICES,
        default="multiple_choice",
    )

    # Mídia para a questão (opcional)
    image = models.ImageField(
        _("imagem"), upload_to="quiz_images/", blank=True, null=True
    )
    video_url = models.URLField(_("URL do vídeo"), blank=True)

    # Pontuação
    points = models.PositiveSmallIntegerField(
        _("pontos"), default=1, help_text=_("Valor em pontos desta questão")
    )

    # Ordem no quiz
    order = models.PositiveIntegerField(_("ordem"))

    # Metadados
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Questão")
        verbose_name_plural = _("Questões")
        ordering = ["quiz", "order"]
        unique_together = [["quiz", "order"]]

    def __str__(self) -> str:
        return f"{self.quiz.title} - Questão {self.order}"

    @property
    def is_multiple_choice(self):
        return self.question_type == "multiple_choice"

    @property
    def is_true_false(self):
        return self.question_type == "true_false"


class Answer(models.Model):
    """
    Modelo representando uma opção de resposta para uma questão.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("questão"),
    )

    text = models.CharField(_("texto da resposta"), max_length=255)
    is_correct = models.BooleanField(_("é correta"), default=False)

    # Para perguntas de ordenação ou associação
    order = models.PositiveSmallIntegerField(
        _("ordem"), default=0, help_text=_("Usado para ordenação ou associação")
    )

    # Explicação para esta resposta
    explanation = models.TextField(
        _("explicação"),
        blank=True,
        help_text=_("Explicação mostrada quando esta resposta é selecionada"),
    )

    class Meta:
        verbose_name = _("Resposta")
        verbose_name_plural = _("Respostas")
        ordering = ["question", "order"]

    def __str__(self) -> str:
        correct_mark = "✓" if self.is_correct else "✗"
        return f"{self.question} - {self.text[:30]} [{correct_mark}]"


class QuizAttempt(models.Model):
    """
    Modelo representando uma tentativa de um aluno em um quiz.
    """

    STATUS_CHOICES = [
        ("in_progress", _("Em Andamento")),
        ("completed", _("Concluído")),
        ("timed_out", _("Tempo Esgotado")),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        verbose_name=_("aluno"),
    )

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts", verbose_name=_("quiz")
    )

    # Status e pontuação
    status = models.CharField(
        _("status"), max_length=20, choices=STATUS_CHOICES, default="in_progress"
    )

    score = models.PositiveSmallIntegerField(_("pontuação"), default=0)

    # Percentual de acertos
    score_percentage = models.DecimalField(
        _("percentual de acertos"), max_digits=5, decimal_places=2, default=0.0
    )

    # Controle de tempo
    started_at = models.DateTimeField(_("iniciado em"), auto_now_add=True)
    completed_at = models.DateTimeField(_("concluído em"), null=True, blank=True)

    class Meta:
        verbose_name = _("Tentativa de Quiz")
        verbose_name_plural = _("Tentativas de Quiz")
        ordering = ["-started_at"]

    def __str__(self) -> str:
        return f"{self.student.get_full_name()} - {self.quiz.title} - {self.score}"

    @property
    def passed(self):
        """Verifica se o aluno passou no quiz conforme a nota mínima definida."""
        return self.score_percentage >= self.quiz.passing_score


class QuestionResponse(models.Model):
    """
    Modelo representando a resposta de um aluno a uma questão específica.
    """

    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name=_("tentativa"),
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name=_("questão"),
    )

    # Para questões de múltipla escolha
    selected_answers = models.ManyToManyField(
        Answer,
        related_name="selected_in",
        verbose_name=_("respostas selecionadas"),
        blank=True,
    )

    # Para questões de texto livre ou vídeo
    text_response = models.TextField(_("resposta em texto"), blank=True)
    video_response_url = models.URLField(_("URL da resposta em vídeo"), blank=True)

    # Avaliação
    is_correct = models.BooleanField(_("está correta"), default=False)
    points_earned = models.PositiveSmallIntegerField(_("pontos obtidos"), default=0)

    # Metadados
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("Resposta à Questão")
        verbose_name_plural = _("Respostas às Questões")
        unique_together = [["attempt", "question"]]

    def __str__(self) -> str:
        return f"{self.attempt.student.get_full_name()} - {self.question}"
