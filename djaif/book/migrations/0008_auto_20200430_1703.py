# Generated by Django 3.0.5 on 2020-04-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20200430_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='bookprogress',
            name='items',
            field=models.ManyToManyField(to='book.Item'),
        ),
    ]
