# Generated by Django 4.1.5 on 2023-01-30 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_generator', '0006_generateddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='generateddata',
            name='rows',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generateddata',
            name='status',
            field=models.CharField(choices=[('processing', ' Processing '), ('ready', ' Ready '), ('error', 'Error ')], default='processing', max_length=15),
        ),
        migrations.AlterField(
            model_name='generateddata',
            name='csv_file',
            field=models.FileField(blank=True, null=True, upload_to='files'),
        ),
    ]
