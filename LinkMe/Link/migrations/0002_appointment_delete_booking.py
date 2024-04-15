# Generated by Django 5.0.3 on 2024-03-31 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Link', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('full_time', models.IntegerField()),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]