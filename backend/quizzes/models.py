"""
Modelos para o app quizzes, definindo estruturas de dados para avaliações e questões.
Otimizado para uso com Supabase como banco de dados.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from typing import Optional

from core.base_models import (
    SupabaseBaseModel, 
    RelatedObjectCache,
    safe_get_related_str_field
)
from courses.models import Lesson, Course


class Quiz(SupabaseBaseModel):
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
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes_created",
        verbose_name=_("criado por"),
    )
    
    # Cache de objetos relacionados
    _course_cache: Optional[RelatedObjectCache[Course]] = None
    _lesson_cache: Optional[RelatedObjectCache[Lesson]] = None
    _created_by_cache: Optional[RelatedObjectCache] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._course_cache = RelatedObjectCache(Course)
        self._lesson_cache = RelatedObjectCache(Lesson)
        self._created_by_cache = RelatedObjectCache(models.Model)

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["course"], name="idx_quiz_course"),
            models.Index(fields=["lesson"], name="idx_quiz_lesson"),
            models.Index(fields=["is_active"], name="idx_quiz_active")
        ]
        db_table = "quizzes"

    def __str__(self) -> str:
        """Representação em string do quiz."""
        return str(self.title)

    @property
    def total_questions(self) -> int:
        """Retorna o número total de questões no quiz."""
        return self.questions.count()

    @property
    def max_score(self) -> int:
        """Retorna a pontuação máxima possível no quiz."""
        return sum(question.points for question in self.questions.all())


class Question(SupabaseBaseModel):
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
        Quiz, 
        on_delete=models.CASCADE, 
        related_name="questions", 
        verbose_name=_("quiz")
    )

    text = models.TextField(_("texto da pergunta"))
    question_type = models.CharField(
        _("tipo de questão"),
        max_length=20,
        choices=TYPE_CHOICES,
        default="multiple_choice",
    )

    # Mídia para a questão (opcional)
    image = models.URLField(
        _("URL da imagem"), 
        blank=True, 
        max_length=500,
        help_text=_("URL para imagem da questão no bucket do Supabase")
    )
    video_url = models.URLField(
        _("URL do vídeo"), 
        blank=True,
        max_length=500
    )

    # Pontuação
    points = models.PositiveSmallIntegerField(
        _("pontos"), 
        default=1, 
        help_text=_("Valor em pontos desta questão")
    )

    # Ordem no quiz
    order = models.PositiveIntegerField(_("ordem"))
    
    # Cache de objetos relacionados
    _quiz_cache: Optional[RelatedObjectCache[Quiz]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quiz_cache = RelatedObjectCache(Quiz)

    class Meta:
        verbose_name = _("Questão")
        verbose_name_plural = _("Questões")
        ordering = ["quiz", "order"]
        unique_together = [["quiz", "order"]]
        indexes = [
            models.Index(fields=["quiz", "order"], name="idx_question_order"),
            models.Index(fields=["question_type"], name="idx_question_type")
        ]
        db_table = "questions"

    def __str__(self) -> str:
        """Representação em string da questão."""
        quiz = self._quiz_cache.get(self, "quiz")
        quiz_title = safe_get_related_str_field(
            quiz, 
            "title", 
            f"Quiz {getattr(self.quiz, 'pk', '')}"
        )
        return f"{quiz_title} - Questão {self.order}"

    @property
    def is_multiple_choice(self) -> bool:
        """Verifica se a questão é de múltipla escolha."""
        return self.question_type == "multiple_choice"

    @property
    def is_true_false(self) -> bool:
        """Verifica se a questão é de verdadeiro/falso."""
        return self.question_type == "true_false"


class Answer(SupabaseBaseModel):
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
        _("ordem"), 
        default=0, 
        help_text=_("Usado para ordenação ou associação")
    )

    # Explicação para esta resposta
    explanation = models.TextField(
        _("explicação"),
        blank=True,
        help_text=_("Explicação mostrada quando esta resposta é selecionada"),
    )
    
    # Cache de objetos relacionados
    _question_cache: Optional[RelatedObjectCache[Question]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._question_cache = RelatedObjectCache(Question)

    class Meta:
        verbose_name = _("Resposta")
        verbose_name_plural = _("Respostas")
        ordering = ["question", "order"]
        indexes = [
            models.Index(fields=["question"], name="idx_answer_question"),
            models.Index(fields=["is_correct"], name="idx_answer_correct")
        ]
        db_table = "answers"

    def __str__(self) -> str:
        """Representação em string da resposta."""
        question = self._question_cache.get(self, "question")
        question_text = ""
        if question:
            question_text = f"Questão {question.order}"
        else:
            question_text = f"Questão {getattr(self.question, 'pk', '')}"
            
        correct_mark = "✓" if self.is_correct else "✗"
        text_preview = self.text[:30] + ("..." if len(self.text) > 30 else "")
        return f"{question_text} - {text_preview} [{correct_mark}]"


class QuizAttempt(SupabaseBaseModel):
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
        Quiz, 
        on_delete=models.CASCADE, 
        related_name="attempts", 
        verbose_name=_("quiz")
    )

    # Status e pontuação
    status = models.CharField(
        _("status"), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="in_progress"
    )

    score = models.PositiveSmallIntegerField(_("pontuação"), default=0)

    # Percentual de acertos
    score_percentage = models.DecimalField(
        _("percentual de acertos"), 
        max_digits=5, 
        decimal_places=2, 
        default=0.0
    )

    # Controle de tempo
    completed_at = models.DateTimeField(
        _("concluído em"), 
        null=True, 
        blank=True
    )
    
    # Metadata adicional
    ip_address = models.GenericIPAddressField(
        _("endereço IP"),
        blank=True,
        null=True,
        help_text=_(
            "Endereço IP usado durante a tentativa"
        )
    )
    
    # Cache de objetos relacionados
    _student_cache: Optional[RelatedObjectCache] = None
    _quiz_cache: Optional[RelatedObjectCache[Quiz]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._student_cache = RelatedObjectCache(models.Model)
        self._quiz_cache = RelatedObjectCache(Quiz)

    class Meta:
        verbose_name = _("Tentativa de Quiz")
        verbose_name_plural = _("Tentativas de Quiz")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student"], name="idx_attempt_student"),
            models.Index(fields=["quiz"], name="idx_attempt_quiz"),
            models.Index(fields=["status"], name="idx_attempt_status"),
            models.Index(fields=["created_at"], name="idx_attempt_date")
        ]
        db_table = "quiz_attempts"

    def __str__(self) -> str:
        """Representação em string da tentativa de quiz."""
        student = self._student_cache.get(self, "student")
        quiz = self._quiz_cache.get(self, "quiz")
        
        student_name = ""
        if student and hasattr(student, 'get_full_name'):
            student_name = student.get_full_name() or str(student)
        else:
            student_name = f"Aluno {getattr(self.student, 'pk', '')}"
            
        quiz_title = safe_get_related_str_field(
            quiz, 
            "title", 
            f"Quiz {getattr(self.quiz, 'pk', '')}"
        )
        
        return f"{student_name} - {quiz_title} - {self.score}"

    @property
    def passed(self) -> bool:
        """Verifica se o aluno passou no quiz conforme a nota mínima definida."""
        quiz = self._quiz_cache.get(self, "quiz")
        if not quiz:
            return False
            
        return self.score_percentage >= quiz.passing_score
        
    def calculate_score(self) -> None:
        """
        Calcula a pontuação e percentual de acertos da tentativa.
        
        Deve ser chamado quando todas as respostas foram registradas.
        """
        from django.db.models import Sum
        
        # Recupera todas as respostas corretas do aluno
        correct_responses = self.responses.filter(
            selected_answers__is_correct=True
        ).distinct()
        
        # Calcula a pontuação total das questões respondidas corretamente
        points = correct_responses.aggregate(
            total=Sum('question__points')
        )['total'] or 0
        
        # Recupera a pontuação máxima possível
        quiz = self._quiz_cache.get(self, "quiz")
        max_points = quiz.max_score if quiz else 0
        
        # Atualiza a pontuação
        self.score = points
        
        # Calcula o percentual de acerto
        if max_points > 0:
            self.score_percentage = (points / max_points) * 100
        else:
            self.score_percentage = 0
            
        self.save(update_fields=['score', 'score_percentage'])


class QuestionResponse(SupabaseBaseModel):
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

    # Para questões de texto livre
    text_response = models.TextField(
        _("resposta em texto"), 
        blank=True,
        help_text=_("Usado para questões de preenchimento ou resposta livre")
    )

    # Para resposta em vídeo
    video_response_url = models.URLField(
        _("URL da resposta em vídeo"), 
        blank=True,
        max_length=500,
        help_text=_(
            "URL para o vídeo de resposta no bucket do Supabase"
        )
    )

    # Metadados
    is_correct = models.BooleanField(
        _("está correta"), 
        default=False,
        help_text=_("Indica se a resposta foi considerada correta")
    )
    
    response_time = models.PositiveIntegerField(
        _("tempo de resposta (segundos)"),
        default=0,
        help_text=_(
            "Tempo que o aluno levou para responder em segundos"
        )
    )
    
    # Cache de objetos relacionados
    _attempt_cache: Optional[RelatedObjectCache[QuizAttempt]] = None
    _question_cache: Optional[RelatedObjectCache[Question]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._attempt_cache = RelatedObjectCache(QuizAttempt)
        self._question_cache = RelatedObjectCache(Question)

    class Meta:
        verbose_name = _("Resposta a Questão")
        verbose_name_plural = _("Respostas a Questões")
        unique_together = [["attempt", "question"]]
        indexes = [
            models.Index(fields=["attempt"], name="idx_response_attempt"),
            models.Index(fields=["question"], name="idx_response_question"),
            models.Index(fields=["is_correct"], name="idx_response_correct")
        ]
        db_table = "question_responses"

    def __str__(self) -> str:
        """Representação em string da resposta do aluno."""
        attempt = self._attempt_cache.get(self, "attempt")
        question = self._question_cache.get(self, "question")
        
        student_name = ""
        if attempt and hasattr(attempt.student, 'get_full_name'):
            student_name = (attempt.student.get_full_name() or 
                           str(attempt.student))
        else:
            student_name = "Aluno"
            
        question_order = getattr(question, 'order', 0) if question else 0
        correct_mark = "✓" if self.is_correct else "✗"
        
        return f"{student_name} - Questão {question_order} [{correct_mark}]"
    
    def check_correctness(self) -> bool:
        """
        Verifica se a resposta está correta e atualiza o status.
        
        Returns:
            bool: True se a resposta estiver correta, False caso contrário.
        """
        question = self._question_cache.get(self, "question")
        if not question:
            self.is_correct = False
            self.save(update_fields=['is_correct'])
            return False
            
        # Verificação baseada no tipo de questão
        is_correct = False
        
        if question.question_type == "multiple_choice":
            # Todas as respostas selecionadas devem ser corretas e todas as
            # respostas corretas devem ser selecionadas
            selected_answers = set(self.selected_answers.all())
            correct_answers = set(Answer.objects.filter(
                question=question, is_correct=True
            ))
            
            is_correct = selected_answers == correct_answers
        
        elif question.question_type == "true_false":
            # Apenas uma resposta deve ser selecionada e deve ser a correta
            selected = self.selected_answers.first()
            is_correct = selected and selected.is_correct
            
        # Outras verificações para outros tipos de perguntas
        # ...
        
        self.is_correct = is_correct
        self.save(update_fields=['is_correct'])
        return is_correct
