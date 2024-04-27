# Generated by Django 4.2.8 on 2024-04-25 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trouble', '0004_commentlike_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('testing', 'Testing'), ('photo_submission', 'Photo Submission')], default=1, max_length=100),
            preserve_default=False,
        ),
    ]