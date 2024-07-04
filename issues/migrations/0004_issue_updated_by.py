# Generated by Django 4.2.13 on 2024-07-03 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issues', '0003_rename_issue_id_comment_issue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]
