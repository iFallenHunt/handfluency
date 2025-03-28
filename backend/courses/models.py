"""
Modelos para o app courses, definindo estruturas de dados para cursos e aulas.
Otimizado para uso com Supabase como banco de dados.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from typing import Optional

from core.base_models import (
    SupabaseBaseModel, 
    RelatedObjectCache,
    safe_get_related_str_field,
    get_display_name
)


class Course(SupabaseBaseModel):
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
        _("nível"), 
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default="basic"
    )
    
    # Mídia do curso
    cover_image = models.URLField(
        _("URL da imagem de capa"), 
        blank=True,
        max_length=500,
        help_text=_("URL para imagem de capa no bucket do Supabase")
    )
    preview_video = models.URLField(
        _("URL do vídeo de prévia"), 
        blank=True,
        max_length=500
    )

    # Metadados
    is_active = models.BooleanField(_("ativo"), default=True)
    is_featured = models.BooleanField(
        _("destacado"), 
        default=False,
        help_text=_("Destaca o curso na página inicial")
    )
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
        _("avaliação média"), 
        max_digits=3, 
        decimal_places=2, 
        default=0.0
    )
    
    # Cache de objetos relacionados
    _created_by_cache: Optional[RelatedObjectCache] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._created_by_cache = RelatedObjectCache(models.Model)

    def __str__(self) -> str:
        """Representação em string do curso."""
        return str(self.title)
        
    def get_absolute_url(self) -> str:
        """URL amigável para o curso."""
        return f"/cursos/{self.slug}/"

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"], name="idx_course_slug"),
            models.Index(fields=["is_active"], name="idx_course_active")
        ]
        db_table = "courses"


class Module(SupabaseBaseModel):
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
    duration_minutes = models.PositiveIntegerField(
        _("duração em minutos"),
        default=0,
        help_text=_("Duração estimada do módulo em minutos")
    )
    
    # Cache de objetos relacionados
    _course_cache: Optional[RelatedObjectCache[Course]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._course_cache = RelatedObjectCache(Course)

    class Meta:
        verbose_name = _("Módulo")
        verbose_name_plural = _("Módulos")
        ordering = ["course", "order"]
        unique_together = [["course", "order"]]
        indexes = [
            models.Index(fields=["course", "order"], name="idx_module_order")
        ]
        db_table = "modules"

    def __str__(self) -> str:
        """Representação em string formatada como 'Curso - Módulo'."""
        course = self._course_cache.get(self, "course")
        course_title = safe_get_related_str_field(
            course, 
            "title", 
            f"Curso {getattr(self.course, 'pk', '')}"
        )
        return f"{course_title} - {self.title}"


class Lesson(SupabaseBaseModel):
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
    video_url = models.URLField(
        _("URL do vídeo"),
        max_length=500,
        help_text=_("URL do vídeo da aula")
    )
    duration = models.PositiveIntegerField(
        _("duração em minutos"), 
        help_text=_("Duração da aula em minutos")
    )
    order = models.PositiveIntegerField(_("ordem"))

    # Metadados
    is_free = models.BooleanField(
        _("é gratuita"),
        default=False,
        help_text=_("Se esta aula está disponível gratuitamente"),
    )
    is_active = models.BooleanField(_("ativa"), default=True)

    # Material complementar
    supplementary_material = models.TextField(
        _("material complementar"),
        blank=True,
        help_text=_("Material adicional para a aula (links, texto, etc)"),
    )
    
    # Recursos adicionais
    attachments = models.JSONField(
        _("anexos"),
        default=list,
        blank=True,
        help_text=_("Lista de anexos em formato JSON com URLs para recursos")
    )

    # Cache de objetos relacionados
    _module_cache: Optional[RelatedObjectCache[Module]] = None
    _course: Optional[Course] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._module_cache = RelatedObjectCache(Module)

    class Meta:
        verbose_name = _("Aula")
        verbose_name_plural = _("Aulas")
        ordering = ["module", "order"]
        unique_together = [["module", "order"]]
        indexes = [
            models.Index(fields=["module", "order"], name="idx_lesson_order"),
            models.Index(fields=["is_free"], name="idx_lesson_free")
        ]
        db_table = "lessons"

    def __str__(self) -> str:
        """Representação em string formatada como 'Curso - Módulo - Aula'."""
        module = self._module_cache.get(self, "module")
        
        if not module:
            return f"Aula {self.order}: {self.title}"
            
        module_title = safe_get_related_str_field(
            module, 
            "title", 
            f"Módulo {getattr(self.module, 'pk', '')}"
        )
        
        # Acessar o curso através do módulo, usando cache do módulo
        course_title = ""
        try:
            course = self.course
            if course:
                course_title = course.title
            else:
                course_title = "Curso"
        except Exception:
            course_title = "Curso"
            
        return f"{course_title} - {module_title} - {self.title}"

    @property
    def course(self) -> Optional[Course]:
        """Retorna o curso a qual esta aula pertence."""
        if self._course:
            return self._course
            
        try:
            module = self._module_cache.get(self, "module")
            if not module:
                return None
                
            course = module._course_cache.get(module, "course")
            self._course = course
            return course
        except Exception:
            return None


class Enrollment(SupabaseBaseModel):
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
    
    # Status da matrícula
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
    
    # Informações adicionais
    completed_at = models.DateTimeField(
        _("completado em"),
        null=True,
        blank=True,
        help_text=_("Data em que o aluno completou o curso")
    )
    
    # Cache de objetos relacionados
    _student_cache: Optional[RelatedObjectCache] = None
    _course_cache: Optional[RelatedObjectCache[Course]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._student_cache = RelatedObjectCache(models.Model)
        self._course_cache = RelatedObjectCache(Course)

    class Meta:
        verbose_name = _("Matrícula")
        verbose_name_plural = _("Matrículas")
        unique_together = [["student", "course"]]
        indexes = [
            models.Index(fields=["student"], name="idx_enrollment_student"),
            models.Index(fields=["course"], name="idx_enrollment_course"),
            models.Index(fields=["is_active"], name="idx_enrollment_active")
        ]
        db_table = "enrollments"

    def __str__(self) -> str:
        """Representação em string formatada como 'Aluno - Curso'."""
        student = self._student_cache.get(self, "student")
        course = self._course_cache.get(self, "course")
        
        student_name = ""
        if student:
            student_name = get_display_name(
                student, 
                "username", 
                f"Aluno {getattr(self.student, 'pk', '')}"
            )
        else:
            student_name = f"Aluno {getattr(self.student, 'pk', '')}"
        
        course_title = safe_get_related_str_field(
            course, 
            "title", 
            f"Curso {getattr(self.course, 'pk', '')}"
        )
        
        return f"{student_name} - {course_title}"


class CourseRating(SupabaseBaseModel):
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
        _("avaliação"), 
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    comment = models.TextField(_("comentário"), blank=True)
    
    # Cache de objetos relacionados
    _student_cache: Optional[RelatedObjectCache] = None
    _course_cache: Optional[RelatedObjectCache[Course]] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._student_cache = RelatedObjectCache(models.Model)
        self._course_cache = RelatedObjectCache(Course)

    class Meta:
        verbose_name = _("Avaliação de curso")
        verbose_name_plural = _("Avaliações de cursos")
        unique_together = [["student", "course"]]
        indexes = [
            models.Index(fields=["student"], name="idx_rating_student"),
            models.Index(fields=["course"], name="idx_rating_course"),
            models.Index(fields=["rating"], name="idx_rating_value")
        ]
        db_table = "course_ratings"

    def __str__(self) -> str:
        """Representação em string da avaliação de curso."""
        student = self._student_cache.get(self, "student")
        course = self._course_cache.get(self, "course")
        
        student_name = ""
        if student:
            student_name = get_display_name(
                student, 
                "username", 
                f"Aluno {getattr(self.student, 'pk', '')}"
            )
        else:
            student_name = f"Aluno {getattr(self.student, 'pk', '')}"
        
        course_title = safe_get_related_str_field(
            course, 
            "title", 
            f"Curso {getattr(self.course, 'pk', '')}"
        )
        
        return f"{course_title} - {self.rating}/5 - {student_name}"
