from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Quiz, Question, Answer, QuizAttempt, QuestionResponse


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    fields = ('text', 'is_correct', 'order', 'explanation')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'order', 'points')
    show_change_link = True


class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    extra = 0
    fields = ('question', 'is_correct', 'points_earned')
    readonly_fields = ('question', 'is_correct', 'points_earned')
    can_delete = False


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'course', 'lesson', 'is_active', 'total_questions',
        'passing_score', 'created_by', 'created_at'
    )
    list_filter = ('is_active', 'course', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'course', 'lesson')
        }),
        (_('Configurações'), {
            'fields': ('is_active', 'time_limit', 'passing_score', 'created_by')
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'text_preview', 'quiz', 'question_type', 'order', 'points'
    )
    list_filter = ('quiz__course', 'quiz', 'question_type')
    search_fields = ('text', 'quiz__title')
    inlines = [AnswerInline]
    fieldsets = (
        (None, {
            'fields': ('quiz', 'text', 'question_type', 'order', 'points')
        }),
        (_('Mídia'), {
            'fields': ('image', 'video_url'),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        """Exibe uma prévia do texto da questão."""
        max_length = 50
        if len(obj.text) > max_length:
            return f"{obj.text[:max_length]}..."
        return obj.text
    text_preview.short_description = _('Questão')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'text_preview', 'question', 'is_correct', 'order'
    )
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text', 'question__text', 'question__quiz__title')
    fieldsets = (
        (None, {
            'fields': ('question', 'text', 'is_correct', 'order')
        }),
        (_('Explicação'), {
            'fields': ('explanation',),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        """Exibe uma prévia do texto da resposta."""
        max_length = 50
        if len(obj.text) > max_length:
            return f"{obj.text[:max_length]}..."
        return obj.text
    text_preview.short_description = _('Resposta')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'quiz', 'status', 'score', 'score_percentage', 
        'started_at', 'completed_at', 'passed'
    )
    list_filter = ('status', 'quiz__course', 'quiz')
    search_fields = (
        'student__username', 'student__first_name', 
        'student__last_name', 'quiz__title'
    )
    readonly_fields = ('started_at',)
    inlines = [QuestionResponseInline]
    fieldsets = (
        (None, {
            'fields': ('student', 'quiz', 'status')
        }),
        (_('Pontuação'), {
            'fields': ('score', 'score_percentage')
        }),
        (_('Tempo'), {
            'fields': ('started_at', 'completed_at')
        }),
    )


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = (
        'attempt_info', 'question_info', 'is_correct',
        'points_earned', 'created_at'
    )
    list_filter = ('is_correct', 'attempt__quiz', 'question__question_type')
    search_fields = (
        'attempt__student__username', 'attempt__student__first_name',
        'attempt__quiz__title', 'question__text'
    )
    filter_horizontal = ('selected_answers',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('attempt', 'question')
        }),
        (_('Resposta'), {
            'fields': ('selected_answers', 'text_response', 'video_response_url')
        }),
        (_('Avaliação'), {
            'fields': ('is_correct', 'points_earned', 'created_at')
        }),
    )
    
    def attempt_info(self, obj):
        """Exibe informações resumidas sobre a tentativa."""
        return f"{obj.attempt.student.get_full_name()} - {obj.attempt.quiz.title}"
    attempt_info.short_description = _('Tentativa')
    
    def question_info(self, obj):
        """Exibe informações resumidas sobre a questão."""
        return f"Q{obj.question.order}: {obj.question.text[:30]}..."
    question_info.short_description = _('Questão')
