# Generated by Django 4.0.3 on 2023-03-30 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('can', '0002_alter_post_title_alter_post_title_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_date', 'id']},
        ),
    ]