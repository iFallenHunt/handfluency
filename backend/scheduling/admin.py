from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import TeacherAvailability, ScheduledClass, ClassNotification


class TeacherAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "get_weekday_display",
        "start_time",
        "end_time",
        "is_active",
    )
    list_filter = ("weekday", "is_active", "teacher")
    search_fields = ("teacher__username", "teacher__first_name", "teacher__last_name")

    def get_weekday_display(self, obj):
        return obj.get_weekday_display()

    get_weekday_display.short_description = _("Dia da Semana")


class ClassNotificationInline(admin.TabularInline):
    model = ClassNotification
    extra = 0
    readonly_fields = ("sent_at", "read", "read_at")
    can_delete = False


class ScheduledClassAdmin(admin.ModelAdmin):
    list_display = ("student", "teacher", "date", "start_time", "end_time", "status")
    list_filter = ("status", "date", "teacher")
    search_fields = (
        "student__username",
        "teacher__username",
        "student__first_name",
        "teacher__first_name",
        "topic",
    )
    readonly_fields = ("created_at", "updated_at")
    inlines = [ClassNotificationInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "student",
                    "teacher",
                    "date",
                    "start_time",
                    "end_time",
                    "status",
                    "topic",
                )
            },
        ),
        (_("Detalhes"), {"fields": ("notes", "meeting_link", "feedback")}),
        (
            _("Informações do Sistema"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


class ClassNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "scheduled_class",
        "recipient",
        "notification_type",
        "sent_at",
        "read",
    )
    list_filter = ("notification_type", "read", "sent_at")
    search_fields = (
        "recipient__username",
        "recipient__first_name",
        "recipient__last_name",
        "message",
    )
    readonly_fields = ("sent_at", "read_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "scheduled_class",
                    "recipient",
                    "notification_type",
                    "message",
                )
            },
        ),
        (_("Status"), {"fields": ("read", "read_at", "sent_at")}),
    )


admin.site.register(TeacherAvailability, TeacherAvailabilityAdmin)
admin.site.register(ScheduledClass, ScheduledClassAdmin)
admin.site.register(ClassNotification, ClassNotificationAdmin)
