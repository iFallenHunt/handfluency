# Generated by Django 5.1.6 on 2025-03-28 17:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0002_initial"),
        ("quizzes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quizzes_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="criado por",
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="lesson",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="quizzes",
                to="courses.lesson",
                verbose_name="aula",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="quizzes.quiz",
                verbose_name="quiz",
            ),
        ),
        migrations.AddField(
            model_name="quizattempt",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attempts",
                to="quizzes.quiz",
                verbose_name="quiz",
            ),
        ),
        migrations.AddField(
            model_name="quizattempt",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quiz_attempts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="aluno",
            ),
        ),
        migrations.AddField(
            model_name="questionresponse",
            name="attempt",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="responses",
                to="quizzes.quizattempt",
                verbose_name="tentativa",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="question",
            unique_together={("quiz", "order")},
        ),
        migrations.AlterUniqueTogether(
            name="questionresponse",
            unique_together={("attempt", "question")},
        ),
    ]
