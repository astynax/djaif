# Generated by Django 3.0.5 on 2021-03-10 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0014_droppeditem'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroppedItemSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookPage')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Item')),
                ('progress_save', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.ProgressSave')),
            ],
        ),
    ]
