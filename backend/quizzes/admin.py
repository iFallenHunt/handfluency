"""
Configuração de admin para o app de quizzes.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Quiz, Question, Answer, QuizAttempt, QuestionResponse


class AnswerInline(admin.TabularInline):
    """Inline para respostas de uma questão."""
    model = Answer
    extra = 3
    fields = ['text', 'is_correct', 'order', 'explanation']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin para gerenciamento de questões."""
    list_display = ['id', 'quiz', 'question_type', 'order', 'points']
    list_filter = ['quiz', 'question_type']
    search_fields = ['text', 'quiz__title']
    inlines = [AnswerInline]
    fieldsets = (
        (None, {
            'fields': ('quiz', 'text', 'question_type', 'order', 'points')
        }),
        (_('Mídia'), {
            'fields': ('image', 'video_url'),
            'classes': ('collapse',),
        }),
    )


class QuestionInline(admin.TabularInline):
    """Inline para questões de um quiz."""
    model = Question
    extra = 0
    fields = ['text', 'question_type', 'order', 'points']
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin para gerenciamento de quizzes."""
    list_display = [
        'id', 'title', 'course', 'lesson', 'is_active', 
        'passing_score', 'time_limit', 'total_questions'
    ]
    list_filter = ['is_active', 'course', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        (_('Relacionamentos'), {
            'fields': ('course', 'lesson', 'created_by')
        }),
        (_('Configurações'), {
            'fields': ('is_active', 'time_limit', 'passing_score')
        }),
    )


class QuestionResponseInline(admin.TabularInline):
    """Inline para respostas de um aluno em um quiz."""
    model = QuestionResponse
    extra = 0
    fields = ['question', 'is_correct', 'text_response', 'response_time']
    readonly_fields = ['is_correct', 'response_time']
    show_change_link = True


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin para gerenciamento de tentativas de quiz."""
    list_display = [
        'id', 'student', 'quiz', 'status', 'score', 
        'score_percentage', 'passed', 'created_at'
    ]
    list_filter = ['status', 'quiz', 'created_at']
    search_fields = [
        'student__username', 'student__email', 
        'quiz__title', 'quiz__course__title'
    ]
    inlines = [QuestionResponseInline]
    readonly_fields = ['score', 'score_percentage', 'passed']
    fieldsets = (
        (None, {
            'fields': ('student', 'quiz', 'status')
        }),
        (_('Pontuação'), {
            'fields': ('score', 'score_percentage', 'passed')
        }),
        (_('Controle de Tempo'), {
            'fields': ('created_at', 'completed_at')
        }),
        (_('Informações Adicionais'), {
            'fields': ('ip_address',),
            'classes': ('collapse',),
        }),
    )


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    """Admin para gerenciamento de respostas a questões."""
    list_display = [
        'id', 'attempt', 'question', 'is_correct', 
        'response_time', 'created_at'
    ]
    list_filter = ['is_correct', 'question__question_type', 'created_at']
    search_fields = [
        'attempt__student__username', 'attempt__student__email',
        'question__text', 'text_response'
    ]
    filter_horizontal = ['selected_answers']
    readonly_fields = ['is_correct']
    fieldsets = (
        (None, {
            'fields': ('attempt', 'question', 'is_correct')
        }),
        (_('Respostas'), {
            'fields': ('selected_answers', 'text_response', 'video_response_url')
        }),
        (_('Metadados'), {
            'fields': ('response_time', 'created_at')
        }),
    )
