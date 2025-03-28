from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from typing import Optional, cast


class Course(models.Model):
    """
    Modelo representando um curso de Libras.
    """

    LEVEL_CHOICES = [
        ("basic", _("Básico")),
        ("intermediate", _("Intermediário")),
        ("advanced", _("Avançado")),
    ]

    title = models.CharField(_("título"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    description = models.TextField(_("descrição"))
    level = models.CharField(
        _("nível"), max_length=20, choices=LEVEL_CHOICES, default="basic"
    )
    cover_image = models.ImageField(
        _("imagem de capa"), upload_to="course_covers/", blank=True, null=True
    )
    preview_video = models.URLField(_("vídeo de prévia"), blank=True)

    # Metadados
    is_active = models.BooleanField(_("ativo"), default=True)
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_created",
        verbose_name=_("criado por"),
    )

    # Estatísticas
    total_students = models.PositiveIntegerField(
        _("total de alunos"), 
        default=0
    )
    average_rating = models.DecimalField(
        _("avaliação média"), max_digits=3, decimal_places=2, default=0.0
    )

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")
        ordering = ["-created_at"]


class Module(models.Model):
    """
    Modelo representando um módulo dentro de um curso.
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name=_("curso"),
    )
    title = models.CharField(_("título"), max_length=200)
    description = models.TextField(_("descrição"))
    order = models.PositiveIntegerField(_("ordem"))

    # Metadados
    is_active = models.BooleanField(_("ativo"), default=True)
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)

    # Cache para objetos relacionados
    _course_cache: Optional[Course] = None

    class Meta:
        verbose_name = _("Módulo")
        verbose_name_plural = _("Módulos")
        ordering = ["course", "order"]
        unique_together = [["course", "order"]]

    def __str__(self) -> str:
        """Representação em string formatada como 'Curso - Módulo'."""
        course_title = ""
        try:
            # Acessar o objeto course diretamente
            course_obj = cast(Course, self.course)
            course_title = course_obj.title
            # Armazenar em cache para uso futuro
            self._course_cache = course_obj
        except Exception:
            course_title = f"Curso {self.course_id}"
        return f"{course_title} - {self.title}"


class Lesson(models.Model):
    """
    Modelo representando uma aula dentro de um módulo.
    """

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("módulo"),
    )
    title = models.CharField(_("título"), max_length=200)
    description = models.TextField(_("descrição"))
    video_url = models.URLField(_("URL do vídeo"))
    duration = models.PositiveIntegerField(
        _("duração em minutos"), help_text=_("Duração da aula em minutos")
    )
    order = models.PositiveIntegerField(_("ordem"))

    # Metadados
    is_free = models.BooleanField(
        _("é gratuita"),
        default=False,
        help_text=_("Se esta aula está disponível gratuitamente"),
    )
    is_active = models.BooleanField(_("ativa"), default=True)
    created_at = models.DateTimeField(_("criada em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizada em"), auto_now=True)

    # Material complementar
    supplementary_material = models.TextField(
        _("material complementar"),
        blank=True,
        help_text=_("Material adicional para a aula (links, texto, etc)"),
    )

    # Cache para objetos relacionados
    _module_cache: Optional[Module] = None

    class Meta:
        verbose_name = _("Aula")
        verbose_name_plural = _("Aulas")
        ordering = ["module", "order"]
        unique_together = [["module", "order"]]

    def __str__(self) -> str:
        """Representação em string formatada como 'Curso - Módulo - Aula'."""
        module_title = ""
        course_title = ""
        try:
            # Acessar o objeto module diretamente
            module_obj = cast(Module, self.module)
            module_title = module_obj.title
            
            # Tentar acessar o curso através do módulo
            course_obj = cast(Course, module_obj.course)
            course_title = course_obj.title
            
            # Armazenar em cache para uso futuro
            self._module_cache = module_obj
            module_obj._course_cache = course_obj
        except Exception:
            module_title = f"Módulo {self.module_id}"
            course_title = "Curso"

        return f"{course_title} - {module_title} - {self.title}"

    @property
    def course(self) -> Optional[Course]:
        """Retorna o curso a qual esta aula pertence."""
        try:
            # Acessar o objeto module diretamente
            module_obj = cast(Module, self.module)
            # Acessar o curso através do módulo
            return cast(Course, module_obj.course)
        except Exception:
            return None


class Enrollment(models.Model):
    """
    Modelo representando a matrícula de um aluno em um curso.
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("aluno"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("curso"),
    )
    enrolled_at = models.DateTimeField(_("matriculado em"), auto_now_add=True)
    is_active = models.BooleanField(_("ativo"), default=True)
    completed = models.BooleanField(_("completo"), default=False)

    # Rastreamento de progresso
    last_accessed = models.DateTimeField(
        _("último acesso"), 
        null=True, 
        blank=True
    )
    progress_percentage = models.PositiveIntegerField(
        _("porcentagem de progresso"), 
        default=0
    )

    class Meta:
        verbose_name = _("Matrícula")
        verbose_name_plural = _("Matrículas")
        unique_together = [["student", "course"]]

    def __str__(self) -> str:
        """Representação em string formatada como 'Aluno - Curso'."""
        student_username = ""
        course_title = ""
        try:
            # Tentar acessar o username do aluno
            user = self.student
            if hasattr(user, 'username'):
                student_username = user.username
            else:
                student_username = str(user)
        except Exception:
            student_username = f"Aluno {self.student_id}"

        try:
            # Tentar acessar o título do curso
            course_obj = cast(Course, self.course)
            course_title = course_obj.title
        except Exception:
            course_title = f"Curso {self.course_id}"

        return f"{student_username} - {course_title}"


class CourseRating(models.Model):
    """
    Modelo para avaliações de cursos pelos alunos.
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_ratings",
        verbose_name=_("aluno"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("curso"),
    )
    rating = models.PositiveSmallIntegerField(
        _("avaliação"), choices=[(i, str(i)) for i in range(1, 6)]
    )
    comment = models.TextField(_("comentário"), blank=True)
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Avaliação de curso")
        verbose_name_plural = _("Avaliações de cursos")
        unique_together = [["student", "course"]]

    def __str__(self) -> str:
        """Representação em string formatada como 'Curso - Avaliação - Aluno'."""
        student_username = ""
        course_title = ""
        try:
            # Tentar acessar o username do aluno
            user = self.student
            if hasattr(user, 'username'):
                student_username = user.username
            else:
                student_username = str(user)
        except Exception:
            student_username = f"Aluno {self.student_id}"

        try:
            # Tentar acessar o título do curso
            course_obj = cast(Course, self.course)
            course_title = course_obj.title
        except Exception:
            course_title = f"Curso {self.course_id}"

        rating_text = f"{course_title} - {self.rating}/5"
        return f"{rating_text} - {student_username}"
