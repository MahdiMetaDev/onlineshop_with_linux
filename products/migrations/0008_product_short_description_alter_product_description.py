# Generated by Django 4.1.4 on 2023-01-07 11:10

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_alter_product_datetime_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="short_description",
            field=models.CharField(
                blank=True, max_length=300, verbose_name="short_description"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=ckeditor.fields.RichTextField(verbose_name="description"),
        ),
    ]
