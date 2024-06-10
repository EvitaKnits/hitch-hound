# Generated by Django 4.2.13 on 2024-06-10 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_text', models.TextField()),
                ('commented_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('issue_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('severity', models.CharField(choices=[('critical', '1 - Critical'), ('high', '2 - High'), ('medium', '3 - Medium'), ('low', '4 - Low')], default='low', max_length=20)),
                ('type', models.CharField(choices=[('bug', 'Bug'), ('missed_requirement', 'Missed Requirement'), ('other', 'Other Issue')], default='bug', max_length=20)),
                ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('testing', 'Testing'), ('approved', 'Approved'), ('closed', 'Closed'), ('cancelled', 'Cancelled')], default='open', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('developer', 'Developer'), ('quality_assurance', 'Quality Assurance'), ('product_manager', 'Product Manager')], max_length=20)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issues.issue')),
            ],
        ),
    ]
