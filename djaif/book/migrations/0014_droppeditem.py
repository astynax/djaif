# Generated by Django 3.0.5 on 2021-03-10 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_progresssave_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroppedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookPage')),
                ('book_progress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookProgress')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Item')),
            ],
        ),
    ]
