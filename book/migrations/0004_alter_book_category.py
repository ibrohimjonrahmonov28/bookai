# Generated by Django 4.2.1 on 2024-02-01 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0003_alter_rating_created_data_alter_rating_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="category",
            field=models.ForeignKey(
                help_text="kategoiya ",
                on_delete=django.db.models.deletion.CASCADE,
                to="book.category",
                verbose_name="book category ",
            ),
        ),
    ]
