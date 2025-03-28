from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Course(models.Model):
    """
    Modelo representando um curso de Libras.
    """
    LEVEL_CHOICES = [
        ('basic', _('Básico')),
        ('intermediate', _('Intermediário')),
        ('advanced', _('Avançado')),
    ]

    title = models.CharField(_('título'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    description = models.TextField(_('descrição'))
    level = models.CharField(
        _('nível'), 
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='basic'
    )
    cover_image = models.ImageField(
        _('imagem de capa'), 
        upload_to='course_covers/', 
        blank=True, 
        null=True
    )
    preview_video = models.URLField(
        _('vídeo de prévia'), 
        blank=True
    )
    
    # Metadados
    is_active = models.BooleanField(_('ativo'), default=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_created',
        verbose_name=_('criado por')
    )
    
    # Estatísticas
    total_students = models.PositiveIntegerField(
        _('total de alunos'), 
        default=0
    )
    average_rating = models.DecimalField(
        _('avaliação média'),
        max_digits=3,
        decimal_places=2,
        default=0.0
    )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = _('Curso')
        verbose_name_plural = _('Cursos')
        ordering = ['-created_at']


class Module(models.Model):
    """
    Modelo representando um módulo dentro de um curso.
    """
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='modules',
        verbose_name=_('curso')
    )
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descrição'))
    order = models.PositiveIntegerField(_('ordem'))
    
    # Metadados
    is_active = models.BooleanField(_('ativo'), default=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Módulo')
        verbose_name_plural = _('Módulos')
        ordering = ['course', 'order']
        unique_together = [['course', 'order']]
    
    def __str__(self) -> str:
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """
    Modelo representando uma aula dentro de um módulo.
    """
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        related_name='lessons',
        verbose_name=_('módulo')
    )
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descrição'))
    video_url = models.URLField(_('URL do vídeo'))
    duration = models.PositiveIntegerField(
        _('duração em minutos'),
        help_text=_('Duração da aula em minutos')
    )
    order = models.PositiveIntegerField(_('ordem'))
    
    # Metadados
    is_free = models.BooleanField(
        _('é gratuita'), 
        default=False,
        help_text=_('Se esta aula está disponível gratuitamente')
    )
    is_active = models.BooleanField(_('ativa'), default=True)
    created_at = models.DateTimeField(_('criada em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizada em'), auto_now=True)
    
    # Material complementar
    supplementary_material = models.TextField(
        _('material complementar'),
        blank=True,
        help_text=_('Material adicional para a aula (links, texto, etc)')
    )
    
    class Meta:
        verbose_name = _('Aula')
        verbose_name_plural = _('Aulas')
        ordering = ['module', 'order']
        unique_together = [['module', 'order']]
    
    def __str__(self) -> str:
        return f"{self.module.course.title} - {self.module.title} - {self.title}"
    
    @property
    def course(self):
        return self.module.course


class Enrollment(models.Model):
    """
    Modelo representando a matrícula de um aluno em um curso.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('aluno')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('curso')
    )
    enrolled_at = models.DateTimeField(_('matriculado em'), auto_now_add=True)
    is_active = models.BooleanField(_('ativo'), default=True)
    completed = models.BooleanField(_('completo'), default=False)
    
    # Rastreamento de progresso
    last_accessed = models.DateTimeField(
        _('último acesso'), 
        null=True, 
        blank=True
    )
    progress_percentage = models.PositiveIntegerField(
        _('porcentagem de progresso'),
        default=0
    )
    
    class Meta:
        verbose_name = _('Matrícula')
        verbose_name_plural = _('Matrículas')
        unique_together = [['student', 'course']]
    
    def __str__(self) -> str:
        return f"{self.student.username} - {self.course.title}"


class CourseRating(models.Model):
    """
    Modelo para avaliações de cursos pelos alunos.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_ratings',
        verbose_name=_('aluno')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name=_('curso')
    )
    rating = models.PositiveSmallIntegerField(
        _('avaliação'),
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    comment = models.TextField(_('comentário'), blank=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Avaliação de curso')
        verbose_name_plural = _('Avaliações de cursos')
        unique_together = [['student', 'course']]
    
    def __str__(self) -> str:
        return f"{self.course.title} - {self.rating}/5 - {self.student.username}"
