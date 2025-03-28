from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from typing import cast

from courses.models import Course, Lesson


class LessonProgress(models.Model):
    """
    Modelo para rastrear o progresso de um aluno em uma aula específica.
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
        verbose_name=_("aluno"),
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="student_progress",
        verbose_name=_("aula"),
    )

    # Status
    STATUS_CHOICES = [
        ("not_started", _("Não Iniciada")),
        ("in_progress", _("Em Andamento")),
        ("completed", _("Concluída")),
    ]

    status = models.CharField(
        _("status"), 
        max_length=20, 
        choices=STATUS_CHOICES,
        default="not_started"
    )

    # Progresso do vídeo em segundos
    video_progress = models.PositiveIntegerField(
        _("progresso do vídeo (segundos)"), 
        default=0
    )

    # Percentual de conclusão (0-100)
    progress_percentage = models.PositiveSmallIntegerField(
        _("percentual de progresso"), 
        default=0
    )

    # Datas de acesso
    last_accessed = models.DateTimeField(_("último acesso"), auto_now=True)

    completed_at = models.DateTimeField(
        _("concluída em"), 
        null=True, 
        blank=True
    )

    # Tempo total assistido em segundos
    total_watched_time = models.PositiveIntegerField(
        _("tempo total assistido (segundos)"), 
        default=0
    )

    # Número de vezes que a aula foi assistida
    view_count = models.PositiveIntegerField(
        _("contagem de visualizações"), 
        default=0
    )

    # Metadados
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("Progresso de Aula")
        verbose_name_plural = _("Progressos de Aulas")
        unique_together = [["student", "lesson"]]
        ordering = ["lesson__module__order", "lesson__order"]

    def __str__(self) -> str:
        """Representação em string do progresso da aula."""
        student_name = ""
        lesson_title = ""
        
        try:
            # Tentar acessar o nome do aluno
            user = self.student
            if hasattr(user, 'get_full_name'):
                student_name = user.get_full_name()
            else:
                student_name = str(user)
        except Exception:
            student_name = f"Aluno {self.student_id}"
            
        try:
            # Tentar acessar o título da aula
            lesson_obj = cast(Lesson, self.lesson)
            lesson_title = lesson_obj.title
        except Exception:
            lesson_title = f"Aula {self.lesson_id}"
            
        status_str = dict(self.STATUS_CHOICES).get(
            self.status, self.status
        )
        
        return f"{student_name} - {lesson_title} - {status_str}"

    @property
    def module(self):
        """Retorna o módulo a qual esta aula pertence."""
        try:
            lesson_obj = cast(Lesson, self.lesson)
            return lesson_obj.module
        except Exception:
            return None

    @property
    def course(self):
        """Retorna o curso a qual esta aula pertence."""
        try:
            lesson_obj = cast(Lesson, self.lesson)
            module = lesson_obj.module
            return module.course
        except Exception:
            return None


class CourseProgress(models.Model):
    """
    Modelo para rastrear o progresso geral de um aluno em um curso.
    Atualizado automaticamente com base no progresso das aulas.
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_progress",
        verbose_name=_("aluno"),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="student_progress",
        verbose_name=_("curso"),
    )

    # Status
    STATUS_CHOICES = [
        ("not_started", _("Não Iniciado")),
        ("in_progress", _("Em Andamento")),
        ("completed", _("Concluído")),
    ]

    status = models.CharField(
        _("status"), 
        max_length=20, 
        choices=STATUS_CHOICES,
        default="not_started"
    )

    # Percentual de conclusão (0-100)
    progress_percentage = models.PositiveSmallIntegerField(
        _("percentual de progresso"), 
        default=0
    )

    # Datas de acesso
    last_accessed = models.DateTimeField(_("último acesso"), auto_now=True)

    completed_at = models.DateTimeField(
        _("concluído em"), 
        null=True, 
        blank=True
    )

    # Métricas de progresso
    completed_lessons = models.PositiveIntegerField(
        _("aulas concluídas"), 
        default=0
    )

    total_lessons = models.PositiveIntegerField(
        _("total de aulas"), 
        default=0
    )

    # Pontuação em quizzes
    quiz_average_score = models.DecimalField(
        _("pontuação média em quizzes"), 
        max_digits=5, 
        decimal_places=2, 
        default=0.0
    )

    # Metadados
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("Progresso de Curso")
        verbose_name_plural = _("Progressos de Cursos")
        unique_together = [["student", "course"]]
        ordering = ["-last_accessed"]

    def __str__(self) -> str:
        """Representação em string do progresso do curso."""
        student_name = ""
        course_title = ""
        
        try:
            # Tentar acessar o nome do aluno
            user = self.student
            if hasattr(user, 'get_full_name'):
                student_name = user.get_full_name()
            else:
                student_name = str(user)
        except Exception:
            student_name = f"Aluno {self.student_id}"
            
        try:
            # Tentar acessar o título do curso
            course_obj = cast(Course, self.course)
            course_title = course_obj.title
        except Exception:
            course_title = f"Curso {self.course_id}"
            
        progress = f"{course_title} - {self.progress_percentage}%"
        return f"{student_name} - {progress}"

    def update_progress(self):
        """
        Atualiza o progresso geral do curso com base no progresso das aulas.
        """
        # Recupera todas as aulas do curso
        lessons = Lesson.objects.filter(
            module__course=self.course
        ).count()

        # Recupera as aulas concluídas pelo aluno
        completed = LessonProgress.objects.filter(
            student=self.student, 
            lesson__module__course=self.course, 
            status="completed"
        ).count()

        # Calcula o percentual de progresso
        if lessons > 0:
            progress = (completed / lessons) * 100
        else:
            progress = 0

        # Atualiza os campos
        self.total_lessons = lessons
        self.completed_lessons = completed
        self.progress_percentage = int(progress)

        # Atualiza o status
        if progress == 0:
            self.status = "not_started"
        elif progress == 100:
            self.status = "completed"
        else:
            self.status = "in_progress"

        self.save()


class Achievement(models.Model):
    """
    Modelo para conquistas e badges que os alunos podem ganhar.
    """

    title = models.CharField(_("título"), max_length=100)
    description = models.TextField(_("descrição"))

    # Tipo de conquista
    TYPE_CHOICES = [
        ("course_completion", _("Conclusão de Curso")),
        ("lesson_streak", _("Sequência de Aulas")),
        ("quiz_score", _("Pontuação em Quiz")),
        ("participation", _("Participação")),
        ("special", _("Especial")),
    ]

    achievement_type = models.CharField(
        _("tipo de conquista"), max_length=20, choices=TYPE_CHOICES
    )

    # Ícone para a conquista
    icon = models.ImageField(
        _("ícone"), upload_to="achievement_icons/", blank=True, null=True
    )

    # Pontos concedidos ao ganhar esta conquista
    points = models.PositiveIntegerField(_("pontos"), default=10)

    # Critérios para conquistar
    requirement_description = models.CharField(
        _("descrição do requisito"),
        max_length=255,
        help_text=_("Ex: Completar 5 aulas consecutivas"),
    )

    # Valor numérico do requisito (se aplicável)
    requirement_value = models.PositiveIntegerField(
        _("valor do requisito"),
        default=1,
        help_text=_("Ex: 5 (para completar 5 aulas)"),
    )

    # Se esta conquista é secreta (só revelada quando conquistada)
    is_secret = models.BooleanField(_("é secreta"), default=False)

    class Meta:
        verbose_name = _("Conquista")
        verbose_name_plural = _("Conquistas")
        ordering = ["achievement_type", "points"]

    def __str__(self) -> str:
        return str(self.title)


class StudentAchievement(models.Model):
    """
    Modelo para rastrear as conquistas obtidas pelos alunos.
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements",
        verbose_name=_("aluno"),
    )

    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="student_achievements",
        verbose_name=_("conquista"),
    )

    # Data em que a conquista foi obtida
    earned_at = models.DateTimeField(_("conquistado em"), auto_now_add=True)

    # Dados relacionados à conquista
    related_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="achievement_records",
        verbose_name=_("curso relacionado"),
    )

    # Se o aluno já visualizou esta conquista
    is_viewed = models.BooleanField(_("visualizado"), default=False)

    class Meta:
        verbose_name = _("Conquista do Aluno")
        verbose_name_plural = _("Conquistas dos Alunos")
        unique_together = [["student", "achievement"]]
        ordering = ["-earned_at"]

    def __str__(self) -> str:
        """Representação em string da conquista do aluno."""
        student_name = ""
        achievement_title = ""
        
        try:
            # Tentar acessar o nome do aluno
            user = self.student
            if hasattr(user, 'get_full_name'):
                student_name = user.get_full_name()
            else:
                student_name = str(user)
        except Exception:
            student_name = f"Aluno {self.student_id}"
            
        try:
            # Tentar acessar o título da conquista
            achievement_obj = cast(Achievement, self.achievement)
            achievement_title = achievement_obj.title
        except Exception:
            achievement_title = f"Conquista {self.achievement_id}"
            
        return f"{student_name} - {achievement_title}"
