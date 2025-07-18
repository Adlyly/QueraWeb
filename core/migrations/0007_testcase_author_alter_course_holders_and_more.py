# Generated by Django 5.2.4 on 2025-07-18 11:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_question_courses_course_questions'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userprofile.userprofile'),
        ),
        migrations.AlterField(
            model_name='course',
            name='holders',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'holder'}, related_name='holder_courses', to='userprofile.userprofile'),
        ),
        migrations.AlterField(
            model_name='course',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='courses', to='core.question'),
        ),
    ]
