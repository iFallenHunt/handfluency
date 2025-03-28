from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0010_alter_group_name_max_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={
                'ordering': ('content_type__app_label', 'content_type__model',
                             'codename'),
                'verbose_name': 'permission',
                'verbose_name_plural': 'permissions'
            },
        ),
    ] 