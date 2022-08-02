# Generated by Django 4.0.4 on 2022-08-02 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField()),
                ('email_address', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=7)),
                ('phone_number', models.IntegerField()),
                ('email_address', models.EmailField(max_length=100)),
                ('age', models.IntegerField()),
                ('photo', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='BreastCancer',
            fields=[
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='statuschecker.patient')),
                ('mean_radius', models.FloatField(max_length=50, null=True)),
                ('mean_area', models.FloatField(max_length=50, null=True)),
                ('mean_concavity', models.FloatField(max_length=50, null=True)),
                ('sensitivity_area', models.FloatField(max_length=50, null=True)),
                ('worst_radius', models.FloatField(max_length=50, null=True)),
                ('worst_perimeter', models.FloatField(max_length=50, null=True)),
                ('worst_area', models.FloatField(max_length=50, null=True)),
                ('worst_concavity', models.FloatField(max_length=50, null=True)),
                ('worst_concave_points', models.FloatField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diabetics',
            fields=[
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='statuschecker.patient')),
                ('no_of_pregnancy', models.FloatField(max_length=50, null=True)),
                ('glucose_level', models.FloatField(max_length=50, null=True)),
                ('blood_pressure', models.FloatField(max_length=50, null=True)),
                ('skin_thickness', models.FloatField(max_length=50, null=True)),
                ('insulin', models.FloatField(max_length=50, null=True)),
                ('bmi', models.FloatField(max_length=50, null=True)),
                ('diabetes_pedigree_function', models.FloatField(max_length=50, null=True)),
                ('age', models.FloatField(max_length=50, null=True)),
            ],
        ),
    ]