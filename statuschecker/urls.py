from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('breast_cancer/', views.breast_cancer, name="breast_cancer"),
   path('breast_cancer_result/', views.breast_cancer_result, name="breast_cancer_result"),
   path('diabetes/', views.diabetes, name="diabetes"),
   path('diabetes_result/', views.diabetes_result, name="diabetes_result"),
   path('login/', views.loginPage, name="login"),
   path('logout/', views.logoutPage, name="logout"),
   path('register/', views.registerPage, name="register"),
   path('patient_registration/', views.registerPatient, name="patient_registration"),
   path('patient_record/', views.lastRegistered, name='patient_record'),
   # path('last_as_current_patient/', views.lastRegisteredAsCurrentPatient, name='last_as_current_patient'),
   path('see_a_patient/', views.SeeAPatientRecord, name='see_a_patient'),
   # path('current_patient/', views.currentPatientById, name='current_patient'),
   path('current_patient_/<str:prk>', views.currentPatient, name='current_patient_'),
   path('bc_registered/<str:prk>/', views.breastCancerTestForRegistered, name='bc_registered'),
   path('d_registered/<str:prk>/', views.diabetesTestForRegistered, name='d_registered'),
   path('edit_patient_record/<str:prk>/', views.editPatientRecord, name='edit_patient_record'),
   path('delete_patient_record/<str:prk>/', views.deletePatientRecord, name='delete_patient_record'),
   path('edit_breast_cancer/<str:prk>/', views.editBCMetricsRecord, name='edit_breast_cancer'),
   path('edit_diabetes/<str:prk>/', views.editDMetricsRecord, name='edit_diabetes'),
   path('create_bc_record/<str:prk>/', views.createBCMetricsRecord, name='create_bc_record'),
   path('create_d_record/<str:prk>/', views.createDMetricsRecord, name='create_d_record'),
   path('list_all_patients/', views.listOfAllPatients, name='list_all_patients'),
   path('about_us/', views.aboutUs, name='about_us'),
   path('contact_us/', views.contactUs, name='contact_us')
]




