# Generated by Django 5.1.6 on 2025-02-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0002_remove_blog_author_alter_blog_createdat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.TextField(default='ghumnesathi'),
        ),
    ]
