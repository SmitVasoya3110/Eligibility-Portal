# Generated by Django 3.1.4 on 2021-01-11 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20210111_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='college', to='exam.college'),
        ),
    ]
