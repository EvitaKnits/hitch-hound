# Generated by Django 4.2.13 on 2024-07-16 15:39

from django.db import migrations, models

def convert_severity(apps, schema_editor):
    Issue = apps.get_model('issues', 'Issue')
    for issue in Issue.objects.all():
        if issue.severity == 'critical':
            issue.severity = 1
        elif issue.severity == 'high':
            issue.severity = 2
        elif issue.severity == 'medium':
            issue.severity = 3
        elif issue.severity == 'low':
            issue.severity = 4
        else:
            issue.severity = 0
        issue.save()

class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_userissue_created_at'),
    ]

    operations = [
        migrations.RunPython(convert_severity),
        migrations.AlterField(
            model_name='issue',
            name='severity',
            field=models.IntegerField(choices=[(1, '1 - Critical'), (2, '2 - High'), (3, '3 - Medium'), (4, '4 - Low')], default=4),
        ),
    ]
