# Generated by Django 5.1.3 on 2024-11-25 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personel', '0002_alter_personel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giriscikis',
            name='cikis_saati',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='giriscikis',
            name='giris_saati',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='AdminIzinAtama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslangic_tarihi', models.DateField()),
                ('bitis_tarihi', models.DateField()),
                ('personel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_izinleri', to='personel.personel')),
            ],
        ),
    ]
