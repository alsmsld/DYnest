# Generated by Django 5.2.4 on 2025-07-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('자유', '자유'), ('공지', '공지'), ('1학년 둥지', '1학년 둥지'), ('2학년 둥지', '2학년 둥지'), ('3학년 둥지', '3학년 둥지')], default='자유', max_length=20),
        ),
    ]
