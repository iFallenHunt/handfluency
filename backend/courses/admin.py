from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Course, Module, Lesson, Enrollment, CourseRating


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "is_active", "created_by", "created_at")
    list_filter = ("level", "is_active", "created_at")
    search_fields = ("title", "description", "created_by__username")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "level",
                    "cover_image",
                    "preview_video",
                )
            },
        ),
        (_("Metadados"), {"fields": ("is_active", "created_by")}),
        (
            _("Estatísticas"),
            {
                "fields": (
                    "total_students",
                    "average_rating",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "is_active")
    list_filter = ("course", "is_active")
    search_fields = ("title", "description", "course__title")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "module",
        "order",
        "duration",
        "is_free",
        "is_active",
    )
    list_filter = ("module__course", "is_free", "is_active")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "module",
                    "title",
                    "description",
                    "video_url",
                    "duration",
                    "order",
                )
            },
        ),
        (_("Configurações"), {"fields": ("is_free", "is_active")}),
        (
            _("Material Complementar"),
            {"fields": ("supplementary_material",), "classes": ("collapse",)},
        ),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "created_at",
        "is_active",
        "completed",
        "progress_percentage",
    )
    list_filter = ("is_active", "completed", "created_at")
    search_fields = ("student__username", "student__email", "course__title")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    list_display = ("course", "student", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("course__title", "student__username", "comment")
    readonly_fields = ("created_at", "updated_at")
