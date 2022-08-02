from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email_address = models.EmailField(max_length=100)

    def __str__(self):
        return self.phone_number


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=7,
                              choices=[
                                  ('Male', 'Male'),
                                  ('Female', 'Female'),
                              ])
    phone_number = models.IntegerField(blank=False, null=False)
    email_address = models.EmailField(max_length=100)
    age = models.IntegerField()
    photo = models.ImageField(upload_to='images')

    def __str__(self):
        return self.first_name


class BreastCancer(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    mean_radius = models.FloatField(max_length=50, null=True)
    mean_area = models.FloatField(max_length=50, null=True, )
    mean_concavity = models.FloatField(max_length=50, null=True)
    mean_concavity = models.FloatField(max_length=50, null=True)
    sensitivity_area = models.FloatField(max_length=50, null=True)
    worst_radius = models.FloatField(max_length=50, null=True)
    worst_perimeter = models.FloatField(max_length=50, null=True)
    worst_area = models.FloatField(max_length=50, null=True)
    worst_concavity = models.FloatField(max_length=50, null=True)
    worst_concave_points = models.FloatField(max_length=50, null=True)

    def __str__(self):
        return self.mean_radius


class Diabetics(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    no_of_pregnancy = models.FloatField(max_length=50, null=True)
    glucose_level = models.FloatField(max_length=50, null=True)
    blood_pressure = models.FloatField(max_length=50, null=True)
    skin_thickness = models.FloatField(max_length=50, null=True)
    insulin = models.FloatField(max_length=50, null=True)
    bmi = models.FloatField(max_length=50, null=True)
    diabetes_pedigree_function = models.FloatField(max_length=50, null=True)
    age = models.FloatField(max_length=50, null=True)

    def __str__(self):
        return self.age
