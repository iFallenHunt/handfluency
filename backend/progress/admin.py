from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    LessonProgress,
    CourseProgress,
    Achievement,
    StudentAchievement,
)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'lesson', 'status', 'progress_percentage',
        'view_count', 'last_accessed'
    )
    list_filter = (
        'status', 'lesson__module__course', 'lesson__module',
        'last_accessed'
    )
    search_fields = (
        'student__username', 'student__first_name',
        'lesson__title', 'lesson__module__title'
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('student', 'lesson', 'status')
        }),
        (_('Progresso'), {
            'fields': (
                'progress_percentage', 'video_progress',
                'total_watched_time', 'view_count'
            )
        }),
        (_('Datas'), {
            'fields': ('last_accessed', 'completed_at', 'created_at')
        }),
    )


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'course', 'status', 'progress_percentage',
        'completed_lessons', 'total_lessons', 'last_accessed'
    )
    list_filter = ('status', 'course', 'last_accessed')
    search_fields = (
        'student__username', 'student__first_name',
        'course__title'
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'status')
        }),
        (_('Progresso'), {
            'fields': (
                'progress_percentage', 'completed_lessons',
                'total_lessons', 'quiz_average_score'
            )
        }),
        (_('Datas'), {
            'fields': ('last_accessed', 'completed_at', 'created_at')
        }),
    )
    actions = ['update_progress']
    
    def update_progress(self, request, queryset):
        for progress in queryset:
            progress.update_progress()
        self.message_user(
            request,
            _(
                'Progresso atualizado para {0} registros.'
                ).format(queryset.count())
        )
    update_progress.short_description = _('Atualizar progresso selecionado')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'achievement_type', 'points', 'requirement_value',
        'is_secret'
    )
    list_filter = ('achievement_type', 'is_secret')
    search_fields = ('title', 'description', 'requirement_description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'achievement_type', 'icon')
        }),
        (_('Requisitos'), {
            'fields': ('requirement_description', 'requirement_value')
        }),
        (_('Recompensas'), {
            'fields': ('points', 'is_secret')
        }),
    )


@admin.register(StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'achievement', 'earned_at', 'related_course',
        'is_viewed'
    )
    list_filter = (
        'achievement__achievement_type', 'earned_at',
        'is_viewed'
    )
    search_fields = (
        'student__username', 'student__first_name',
        'achievement__title', 'related_course__title'
    )
    readonly_fields = ('earned_at',)
    fieldsets = (
        (None, {
            'fields': ('student', 'achievement', 'related_course')
        }),
        (_('Status'), {
            'fields': ('is_viewed', 'earned_at')
        }),
    )
