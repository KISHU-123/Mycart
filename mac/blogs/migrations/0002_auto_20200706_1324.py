# Generated by Django 3.0.7 on 2020-07-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='chead0',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.AlterField(
            model_name='blog',
            name='chead1',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.AlterField(
            model_name='blog',
            name='chead2',
            field=models.CharField(default='', max_length=700),
        ),
        migrations.AlterField(
            model_name='blog',
            name='head0',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AlterField(
            model_name='blog',
            name='head1',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AlterField(
            model_name='blog',
            name='head2',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default='', max_length=70),
        ),
    ]
