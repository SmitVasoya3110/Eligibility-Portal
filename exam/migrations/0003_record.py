# Generated by Django 3.1.2 on 2020-10-27 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_question_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=10)),
                ('exam_id', models.CharField(max_length=10)),
                ('question_id', models.CharField(max_length=10)),
                ('answer', models.CharField(default='N', max_length=1)),
            ],
        ),
    ]
