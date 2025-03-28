# Generated by Django 5.1.6 on 2025-03-28 17:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(
                    max_length=100, verbose_name="nome"
                    )),
                ("description", models.TextField(verbose_name="descrição")),
                (
                    "badge_image",
                    models.ImageField(
                        upload_to="achievement_badges/",
                        verbose_name="imagem da insígnia",
                    ),
                ),
                (
                    "required_points",
                    models.PositiveIntegerField(
                        default=0, verbose_name="pontos necessários"
                    ),
                ),
                (
                    "achievement_type",
                    models.CharField(
                        choices=[
                            ("course_completion", "Conclusão de Curso"),
                            ("streak", "Sequência de Dias"),
                            ("quiz_mastery", "Domínio de Quizzes"),
                            ("video_completion", "Conclusão de Vídeos"),
                            ("participation", "Participação em Aulas ao Vivo"),
                        ],
                        max_length=50,
                        verbose_name="tipo de conquista",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="criado em"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="atualizado em"
                    ),
                ),
            ],
            options={
                "verbose_name": "Conquista",
                "verbose_name_plural": "Conquistas",
                "ordering": ["required_points"],
            },
        ),
        migrations.CreateModel(
            name="CourseProgress",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "progress_percentage",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="porcentagem de progresso"
                    ),
                ),
                (
                    "completed_modules",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="módulos completados"
                    ),
                ),
                (
                    "total_modules",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="total de módulos"
                    ),
                ),
                (
                    "completed_lessons",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="aulas completadas"
                    ),
                ),
                (
                    "total_lessons",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="total de aulas"
                    ),
                ),
                (
                    "last_accessed",
                    models.DateTimeField(
                        auto_now=True, verbose_name="último acesso"
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="iniciado em"
                    ),
                ),
                (
                    "completed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="completado em"
                    ),
                ),
                (
                    "streak_days",
                    models.PositiveIntegerField(
                        default=0, verbose_name="dias consecutivos"
                    ),
                ),
                (
                    "total_points",
                    models.PositiveIntegerField(
                        default=0, verbose_name="pontos totais"
                    ),
                ),
            ],
            options={
                "verbose_name": "Progresso do Curso",
                "verbose_name_plural": "Progressos dos Cursos",
                "ordering": ["-last_accessed"],
            },
        ),
        migrations.CreateModel(
            name="LessonProgress",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "is_completed",
                    models.BooleanField(
                        default=False, verbose_name="completa"
                    ),
                ),
                (
                    "progress_percentage",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="porcentagem de progresso"
                    ),
                ),
                (
                    "last_position",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Posição em segundos no vídeo",
                        verbose_name="última posição",
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="iniciado em"
                    ),
                ),
                (
                    "completed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="completado em"
                    ),
                ),
                (
                    "last_accessed",
                    models.DateTimeField(
                        auto_now=True, verbose_name="último acesso"
                    ),
                ),
            ],
            options={
                "verbose_name": "Progresso da Aula",
                "verbose_name_plural": "Progressos das Aulas",
                "ordering": ["-last_accessed"],
            },
        ),
        migrations.CreateModel(
            name="StudentAchievement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "earned_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="conquistado em"
                    ),
                ),
                (
                    "points_earned",
                    models.PositiveIntegerField(
                        default=0, verbose_name="pontos ganhos"
                    ),
                ),
                (
                    "is_seen",
                    models.BooleanField(
                        default=False, verbose_name="visualizada"
                    ),
                ),
            ],
            options={
                "verbose_name": "Conquista do Aluno",
                "verbose_name_plural": "Conquistas dos Alunos",
                "ordering": ["-earned_at"],
            },
        ),
    ]
