from django.shortcuts import render, redirect, reverse
from .ml_codes.breast_cancer import BreastCancerTest
from .ml_codes.diabetes import DiabetesTest

# login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from django.contrib.messages import constants as messages

# form
from .forms import PatientForm, BreastCancerForm, DiabeticsForm
from .models import Patient, BreastCancer, Diabetics

# query
from django.db.models import Q

# bc_result is the dictionary that contains all the required information obtained during prediction for breast_cancer
# d_result is the dictionary that contains all the required information obtained during prediction for diabetes

# x1 = 0
bc_result = {}
d_result = {}
checker = True
print(checker)
x_s = []
current_patient = None
pk = ""


# This is the home view
def index(request):
    home = True
    context = {'home': home}
    return render(request, 'base/index.html', context)


# This is the form for breast cancer inputs from non-registered patients.
def breast_cancer(request):

    global bc_result, checker

    if request.method == 'POST':
        x1 = request.POST['mean_radius']
        x2 = request.POST.get('mean_area')
        x3 = request.POST.get('mean_concavity')
        x4 = request.POST.get('mean_concave_point')
        x5 = request.POST.get('sensitivity_area')
        x6 = request.POST.get('worst_radius')
        x7 = request.POST.get('worst_perimeter')
        x8 = request.POST.get('worst_area')
        x9 = request.POST.get('worst_concavity')
        x10 = request.POST.get('worst_concave_points')

        global x_s
        x_s = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]
        print('pres-ult', x_s)

        # verifying if the imputed numbers are valid floats
        x = [True for i in x_s if (i.isnumeric or i.isspace is False) and i != ""]
        print('result', x)
        if len(x) == 10:
            new_case = BreastCancerTest()

            bc_result = new_case.predictor([float(i) for i in [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]])
            print('breast cancer result', bc_result)
            return redirect("breast_cancer_result")
        else:
            checker = False
            redirect('breast_cancer')

    context = {
        'checker': checker,
        'home': False,
    }
    return render(request, 'base/breast_cancer.html', context)


# This displays the result for non-registered patients
def breast_cancer_result(request):
    header ="cross"
    context = { 'b': bc_result, 'checker': checker, 'header': header}
    return render(request, 'base/breast_cancer_result.html', context)


# This displays the form for diabetes input for non-registered patients.
def diabetes(request):
    global d_result, checker, header
    header = "cross"

    if request.method == 'POST':
        x1 = request.POST['no_of_pregnancies']
        x2 = request.POST.get('glucose_level')
        x3 = request.POST.get('blood_pressure')
        x4 = request.POST.get('skin_thickness')
        x5 = request.POST.get('insulin')
        x6 = request.POST.get('bmi')
        x7 = request.POST.get('pedigree')
        x8 = request.POST.get('age')

        global x_s
        x_s = [x1, x2, x3, x4, x5, x6, x7, x8]
        print('pres-ult', x_s)

        # verifying if the imputed numbers are valid floats
        x = [True for i in x_s if (i.isnumeric or i.isspace is False) and i != ""]
        print('result', x)
        if len(x) >= 3:
            new_case = DiabetesTest()
            d_result = new_case.predictor([float(i) for i in [x2, x6, x8]])
            print('diabetes result', d_result)
            return redirect("diabetes_result")
        else:
            checker = False
            redirect('diabetes')

    context = {
        'checker': checker, 'home': False
    }
    return render(request, 'base/diabetes.html', context)


# This displays the diabetes test result for non-registered patients
def diabetes_result(request):

    context = {'b': d_result, 'checker': checker, 'home': False}
    return render(request, 'base/diabetes_result.html', context)


# login page for doctors
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)

        except:
            # messages.error(request, "user is non-existent")
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "User or password does not exist")

    page = "login"
    context = {'home': False,
               'page': page
               }
    return render(request, "base/login_register.html", context)


# logout view for doctors
@login_required
def logoutPage(request):
    logout(request)

    return redirect('index')


# takes care of registration for doctors
def registerPage(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        form = UserCreationForm(request.POST)
        if form.is_valid() and (username not in str(password)) and (username not in str(password2)):
            user = form.save(commit=False)
            user.save()

            login(request, user)
            return redirect("index")

        else:
            messages.error(request, "Password should be strong and must match")

    context = {
        'page': page,
        'form': form
       }
    return render(request, 'base/login_register.html', context)


# Takes care of registration for patients
@login_required
def registerPatient(request):
    form = PatientForm()
    success = False
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            # email_address = request.POST.get("email_address")
            # if not Patient.objects.filter(email_address=email_address)
            form.save()
            return redirect("patient_record")

        else:
            messages.error(request, "patient Registration not successful")
            # return redirect("")

    context = {'form': form, 'success': success}
    return render(request, 'base/patient_registration.html', context)


# display the last patient as the current patient.
'''@login_required
def lastRegisteredAsCurrentPatient(request):
    global current_patient
    patient = current_patient
    context = {
        'patient': patient
        }
    return render(request, 'base/last_as_current_patient.html', context)
'''

# The last patient who was registered


@login_required
def lastRegistered(request):
    patient = Patient.objects.latest('id')
    global current_patient
    current_patient = patient
    context = {
        'patient': patient
    }
    return render(request, 'base/last_patient_record.html', context)


# When a patient's record is to be accessed
@login_required
def SeeAPatientRecord(request):
    patients = None
    specific_patient = None

    if request.method == "POST":
        q = request.POST.get('q').strip()
        q = q if q is not None else ''
        if 'mlhc-nig/' in q.lower():
            q = q.lower().strip('mlhc-nig/').strip()
        else:
            q = q

        if not q.isnumeric():
            patients = Patient.objects.filter(email_address=q)
            if patients:
                pass
            else:
                messages.error(request, "No Patient Found")

        else:
            specific_patient = Patient.objects.filter(id=q)
            if specific_patient:
                global pk
                pk = q
                return redirect(reverse("current_patient_", args=(specific_patient[0].id,)))
            else:
                messages.error(request, "No Patient Found")

    context = {'patients': patients, 'patient': specific_patient}
    return render(request, 'base/see_a_patient_record.html', context)


# this function is visited if id is used to find patient from the SeeAPatientRecord function
'''@login_required
def currentPatientById(request):
    global pk
    patient = Patient.objects.get(id=pk)
    bc_record = BreastCancer.objects.filter(patient_id=pk)
    d_record = Diabetics.objects.filter(patient_id=pk)

    context = {'patient': patient,
               'bc_record': bc_record,
               'd_record': d_record,
               }

    return render(request, 'base/current_patient_.html', context)
'''


# this function is visited if email or id is used to find patient from the SeeAPatientRecord function
@login_required
def currentPatient(request, prk):
    patient = Patient.objects.get(id=prk)
    bc_record = BreastCancer.objects.filter(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    context = {'patient': patient,
               'bc_record': bc_record,
               'd_record': d_record}
    return render(request, 'base/current_patient_.html', context)


# Conducts breast cancer test for registered patients.
@login_required
def breastCancerTestForRegistered(request, prk):
    bc_record = BreastCancer.objects.get(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    patient = Patient.objects.get(id=prk)
    b = bc_record

    x1 = b.mean_radius
    x2 = b.mean_area
    x3 = b.mean_concavity
    x4 = b.mean_concavity
    x5 = b.sensitivity_area
    x6 = b.worst_radius
    x7 = b.worst_perimeter
    x8 = b.worst_area
    x9 = b.worst_concavity
    x10 = b.worst_concave_points

    new_case = BreastCancerTest()
    bc_result_r = new_case.predictor([float(x) for x in [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]])
    context = {
        'checker': checker,
        'home': False,
        'patient': patient,
        'd_record': d_record,
        'bc_record': bc_record,
        'bc_result': bc_result_r
    }
    return render(request, 'base/bc_test_registered.html', context)


# Conducts diabetes test for registered patients.
@login_required
def diabetesTestForRegistered(request, prk):
    d_record = Diabetics.objects.get(patient_id=prk)
    bc_record = BreastCancer.objects.filter(patient_id=prk)
    patient = Patient.objects.get(id=prk)
    b = d_record

    x1 = b.no_of_pregnancy
    x2 = b.glucose_level
    x3 = b.blood_pressure
    x4 = b.skin_thickness
    x5 = b.insulin
    x6 = b.bmi
    x7 = b.diabetes_pedigree_function
    x8 = patient.age

    new_case = DiabetesTest()
    d_result_r = new_case.predictor([float(x) for x in [x2, x6, x8]])
    context = {
        'checker': checker,
        'home': False,
        'patient': patient,
        'd_record': d_record,
        'bc_record': bc_record,
        'd_result': d_result_r
    }
    return render(request, 'base/d_test_registered.html', context)


# To edit a patient's record -  a patient who is the current patient
@login_required
def editPatientRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    form = PatientForm(instance=patient)

    bc_record = BreastCancer.objects.filter(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            # return redirect("index")
            context = {

            }
            return redirect(reverse("current_patient_", args=(patient.id,)))


    context = {
        'patient': patient,
        'form': form,
        'bc_record': bc_record,
        'd_record': d_record
    }
    return render(request, 'base/edit_patient_record.html', context)


# to delete a patient's record
@login_required
def deletePatientRecord(request, prk):
    patient = Patient.objects.get(id=prk)

    bc_record = BreastCancer.objects.filter(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    if request.method == "POST":
        patient.delete()
        return redirect("see_a_patient")

    context = {'patient': patient,
               'bc_record': bc_record,
               'd_record': d_record}
    return render(request, 'base/delete_patient_record.html', context)


# Edit patient's breast cancer record
@login_required
def editBCMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    bc_record = BreastCancer.objects.get(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    form = BreastCancerForm(instance=bc_record)
    if request.method == 'POST':
        form = BreastCancerForm(request.POST, instance=bc_record)
        if form.is_valid():
            form.save()
            return redirect(reverse("current_patient_", args=(patient.id,)))

    context = {
            'form': form,
            'patient': patient,
            'bc_record': bc_record,
            'd_record': d_record
        }
    return render(request, 'base/edit_breast_cancer.html', context)


# edit patient's diabetes record
@login_required
def editDMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    d_record = Diabetics.objects.get(patient_id=prk)

    form = DiabeticsForm(instance=d_record)
    if request.method == 'POST':
        form = DiabeticsForm(request.POST, instance=d_record)
        if form.is_valid():
            form.save()
            return redirect(reverse("current_patient_", args=(patient.id,)))

    context = {'form': form,
               'patient': patient,
               'bc_case': d_record
               }
    return render(request, 'base/edit_diabetes.html', context)


# create patient's breast cancer record
@login_required
def createBCMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    form = BreastCancerForm()
    if request.method == 'POST':
        new_bc_record = BreastCancer(patient_id=prk, patient=patient)
        new_bc_record.save()
        form = BreastCancerForm(request.POST, instance=new_bc_record)
        if form.is_valid():
            form.save()
            return redirect(reverse("current_patient_", args=(patient.id,)))

    context = {'patient': patient,
               'form': form,
               'd_record': d_record}
    return render(request, 'base/create_bc_record.html', context)


# creates patient's diabetes record
@login_required
def createDMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    bc_record = BreastCancer.objects.filter(patient_id=prk)
    form = DiabeticsForm()

    if request.method == 'POST':
        new_d_record = Diabetics(patient_id=prk, patient=patient)
        new_d_record.save()
        form = DiabeticsForm(request.POST, instance=new_d_record)
        if form.is_valid():
            form.save()
            return redirect(reverse("current_patient_", args=(patient.id,)))

    context = {'patient': patient,
               'form': form,
               'bc_record': bc_record}
    return render(request, 'base/create_d_record.html', context)


# List all registered patients.
@login_required
def listOfAllPatients(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'base/list_all_patients.html', context)


print('checker', checker)


# About us
def aboutUs(request):
    home = True
    context = {
        'home': home
    }
    return render(request, 'base/about_us.html', context)


# Contact us
def contactUs(request):
    home = True
    context = {
        'home': home
    }
    return render(request, 'base/contact_us.html', context)



"""from django.shortcuts import render, redirect
from .ml_codes.breast_cancer import BreastCancerTest
from .ml_codes.diabetics import DiabeticsTest

# login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from django.contrib.messages import constants as messages

# form
from .forms import PatientForm, BreastCancerForm, DiabeticsForm
from .models import Patient, BreastCancer, Diabetics

# query
from django.db.models import Q

# bc_result is the dictionary that contains all the required information obtained during prediction for breast_cancer
# d_result is the dictionary that contains all the required information obtained during prediction for diabetics

# x1 = 0
bc_result = {}
d_result = {}
checker = True
print(checker)
x_s = []
current_patient = None
pk = ""

# This is the home view
def index(request):
    home = True
    context = {'home': home}
    return render(request, 'base/index.html', context)


# This is the form for breast cancer inputs from non-registered patients.
def breast_cancer(request):

    global bc_result, checker

    if request.method == 'POST':
        x1 = request.POST['mean_radius']
        x2 = request.POST.get('mean_area')
        x3 = request.POST.get('mean_concavity')
        x4 = request.POST.get('mean_concave_point')
        x5 = request.POST.get('sensitivity_area')
        x6 = request.POST.get('worst_radius')
        x7 = request.POST.get('worst_perimeter')
        x8 = request.POST.get('worst_area')
        x9 = request.POST.get('worst_concavity')
        x10 = request.POST.get('worst_concave_points')

        global x_s
        x_s = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]
        print('pres-ult', x_s)

        # verifying if the imputed numbers are valid floats
        x = [True for i in x_s if (i.isnumeric or i.isspace is False) and i != ""]
        print('result', x)
        if len(x) == 10:
            new_case = BreastCancerTest()

            bc_result = new_case.predictor([float(i) for i in [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]])
            print('breast cancer result', bc_result)
            return redirect("breast_cancer_result")
        else:
            checker = False
            redirect('breast_cancer')

    context = {
        'checker': checker,
        'home': False,
    }
    return render(request, 'base/breast_cancer.html', context)


# This displays the result for non-registered patients
def breast_cancer_result(request):
    header ="cross"
    context = { 'b': bc_result, 'checker': checker, 'header': header}
    return render(request, 'base/breast_cancer_result.html', context)


# This displays the form for diabetics input for non-registered patients.
def diabetics(request):
    global d_result, checker, header
    header = "cross"

    if request.method == 'POST':
        x1 = request.POST['no_of_pregnancies']
        x2 = request.POST.get('glucose_level')
        x3 = request.POST.get('blood_pressure')
        x4 = request.POST.get('skin_thickness')
        x5 = request.POST.get('insulin')
        x6 = request.POST.get('bmi')
        x7 = request.POST.get('pedigree')
        x8 = request.POST.get('age')

        global x_s
        x_s = [x1, x2, x3, x4, x5, x6, x7, x8]
        print('pres-ult', x_s)

        # verifying if the imputed numbers are valid floats
        x = [True for i in x_s if (i.isnumeric or i.isspace is False) and i != ""]
        print('result', x)
        if len(x) >= 3:
            new_case = DiabeticsTest()
            d_result = new_case.predictor([float(i) for i in [x2, x6, x8]])
            print('diabetics result', d_result)
            return redirect("diabetics_result")
        else:
            checker = False
            redirect('diabetics')

    context = {
        'checker': checker, 'home': False
    }
    return render(request, 'base/diabetes.html', context)


# This displays the diabetics test result for non-registered patients
def diabetics_result(request):

    context = {'b': d_result, 'checker': checker, 'home': False}
    return render(request, 'base/diabetes_result.html', context)


# login page for doctors
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)

        except:
            # messages.error(request, "user is non-existent")
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "User or password does not exist")

    page = "login"
    context = {'home': False,
               'page': page
               }
    return render(request, "base/login_register.html", context)


# logout view for doctors
@login_required
def logoutPage(request):
    logout(request)

    return redirect('index')


# takes care of registration for doctors
@login_required
def registerPage(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            login(request, user)
            return redirect("index")
        else:
            messages.error(request, 'Registration not successful, try again')

    context = {
        'page': page,
        'form': form
       }
    return render(request, 'base/login_register.html', context)


# Takes care of registration for patients
@login_required
def registerPatient(request):
    form = PatientForm()
    success = False
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            # email_address = request.POST.get("email_address")
            # if not Patient.objects.filter(email_address=email_address)
            form.save()
            return redirect("patient_record")

        else:
            messages.error(request, "patient Registration not successful")
            # return redirect("")

    context = {'form': form, 'success': success}
    return render(request, 'base/patient_registration.html', context)


# display the last patient as the current patient.
@login_required
def lastRegisteredAsCurrentPatient(request):
    global current_patient
    patient = current_patient
    context = {
        'patient': patient
        }
    return render(request, 'base/last_as_current_patient.html', context)


# The last patient who was registered
@login_required
def lastRegistered(request):
    patient = Patient.objects.latest('id')
    global current_patient
    current_patient = patient
    context = {
        'patient': patient
    }
    return render(request, 'base/last_patient_record.html', context)


# When a patient's record is to be accessed
@login_required
def SeeAPatientRecord(request):
    patients = None
    specific_patient = None

    if request.method == "POST":
        q = request.POST.get('q').strip()
        q = q if q is not None else ''
        if 'mlhc-nig/' in q.lower():
            q = q.lower().strip('mlhc-nig/').strip()
        else:
            q = q

        if not q.isnumeric():
            patients = Patient.objects.filter(email_address=q)
            if patients:
                pass
            else:
                messages.error(request, "No Patient Found")

        else:
            patient = Patient.objects.filter(id=q)
            if patient:
                '''global pk
                pk = q'''
                return redirect("current_patient")
            else:
                messages.error(request, "No Patient Found")

    context = {'patients': patients, 'patient': patient}
    return render(request, 'base/see_a_patient_record.html', context)


# this function is visited if id is used to find patient from the SeeAPatientRecord function
@login_required
def currentPatientById(request):
    global pk
    patient = Patient.objects.get(id=pk)
    bc_record = BreastCancer.objects.filter(patient_id=pk)
    d_record = Diabetics.objects.filter(patient_id=pk)

    context = {'patient': patient,
               'bc_record': bc_record,
               'd_record': d_record,
               }

    return render(request, 'base/current_patient_.html', context)


# this function is visited if email or id is used to find patient from the SeeAPatientRecord function
@login_required
def currentPatientByEmail(request, prk):
    patient = Patient.objects.get(id=prk)
    bc_record = BreastCancer.objects.filter(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    context = {'patient': patient,
               'bc_record': bc_record,
               'd_record': d_record}
    return render(request, 'base/current_patient_.html', context)


# Conducts breast cancer test for registered patients.
@login_required
def breastCancerTestForRegistered(request, prk):
    bc_record = BreastCancer.objects.get(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    patient = Patient.objects.get(id=prk)
    b = bc_record

    x1 = b.mean_radius
    x2 = b.mean_area
    x3 = b.mean_concavity
    x4 = b.mean_concavity
    x5 = b.sensitivity_area
    x6 = b.worst_radius
    x7 = b.worst_perimeter
    x8 = b.worst_area
    x9 = b.worst_concavity
    x10 = b.worst_concave_points

    new_case = BreastCancerTest()
    bc_result_r = new_case.predictor([float(x) for x in [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]])
    context = {
        'checker': checker,
        'home': False,
        'patient': patient,
        'd_record': d_record,
        'bc_record': bc_record,
        'bc_result': bc_result_r
    }
    return render(request, 'base/bc_test_registered.html', context)


# Conducts diabetics test for registered patients.
@login_required
def diabeticsTestForRegistered(request, prk):
    d_record = Diabetics.objects.get(patient_id=prk)
    bc_record = BreastCancer.objects.get(patient_id=prk)
    patient = Patient.objects.get(id=prk)
    b = d_record

    x1 = b.no_of_pregnancy
    x2 = b.glucose_level
    x3 = b.blood_pressure
    x4 = b.skin_thickness
    x5 = b.insulin
    x6 = b.bmi
    x7 = b.diabetics_pedigree_function
    x8 = b.age

    new_case = DiabeticsTest()
    d_result_r = new_case.predictor([float(x) for x in [x2, x6, x8]])
    context = {
        'checker': checker,
        'home': False,
        'patient': patient,
        'd_record': d_record,
        'bc_record': bc_record,
        'd_result': d_result_r
    }
    return render(request, 'base/d_test_registered.html', context)


# To edit a patient's record -  a patient who is the current patient
@login_required
def editPatientRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    form = PatientForm(instance=patient)

    bc_record = BreastCancer.objects.filter(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("current_patient")

    context = {
        'patient': patient,
        'form': form,
        'bc_record': bc_record,
        'd_record': d_record
    }
    return render(request, 'base/edit_patient_record.html', context)



@login_required
def deletePatientRecord(request, prk):
    patient = Patient.objects.get(id=prk)

    bc_record = BreastCancer.objects.filter(patient_id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    if request.method == "POST":
        patient.delete()
        return redirect("see_a_patient")

    context = {'patient': patient,
               'bc_record': bc_record,
               'd_record': d_record}
    return render(request, 'base/delete_patient_record.html', context)


@login_required
def editBCMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    bc_record = BreastCancer.objects.get(patient_id=prk)
    d_record = Diabetics.objects.get(patient_id=prk)

    form = BreastCancerForm(instance=bc_record)
    if request.method == 'POST':
        form = BreastCancerForm(request.POST, instance=bc_record)
        if form.is_valid():
            form.save()
            return redirect("current_patient")

    context = {
            'form': form,
            'patient': patient,
            'bc_record': bc_record,
            'd_record': d_record
        }
    return render(request, 'base/edit_breast_cancer.html', context)


# editDMetricsRecord means edit diabetics record
@login_required
def editDMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    d_record = Diabetics.objects.get(patient_id=prk)

    form = DiabeticsForm(instance=d_record)
    if request.method == 'POST':
        form = DiabeticsForm(request.POST, instance=d_record)
        if form.is_valid():
            form.save()
            return redirect("current_patient")

    context = {'form': form,
               'patient': patient,
               'bc_case': d_record
               }
    return render(request, 'base/edit_diabetes.html', context)


@login_required
def createBCMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    d_record = Diabetics.objects.filter(patient_id=prk)

    form = BreastCancerForm()
    if request.method == 'POST':
        new_bc_record = BreastCancer(patient_id=prk, patient=patient)
        new_bc_record.save()
        form = BreastCancerForm(request.POST, instance=new_bc_record)
        if form.is_valid():
            form.save()
            return redirect("current_patient")

    context = {'patient': patient,
               'form': form,
               'd_record':d_record}
    return render(request, 'base/create_bc_record.html', context)


@login_required
def createDMetricsRecord(request, prk):
    patient = Patient.objects.get(id=prk)
    bc_record = BreastCancer.objects.filter(patient_id=prk)
    form = DiabeticsForm()

    if request.method == 'POST':
        new_d_record = Diabetics(patient_id=prk, patient=patient)
        new_d_record.save()
        form = DiabeticsForm(request.POST, instance=new_d_record)
        if form.is_valid():
            form.save()
            return redirect("current_patient")

    context = {'patient': patient,
               'form': form,
               'bc_record': bc_record}
    return render(request, 'base/create_d_record.html', context)


@login_required
def listOfAllPatients(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'base/list_all_patients.html', context)


print('checker', checker)


def aboutUs(request):
    home = True
    context = {
        'home': home
    }
    return render(request, 'base/about_us.html', context)


def contactUs(request):
    home = True
    context = {
        'home': home
    }
    return render(request, 'base/contact_us.html', context)
    """