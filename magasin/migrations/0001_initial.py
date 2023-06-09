# Generated by Django 4.1.7 on 2023-03-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.TextField(default='Non defini')),
                ('type', models.CharField(choices=[('em', 'Emballé'), ('fr', 'Frais'), ('cs', 'Conservé')], max_length=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
