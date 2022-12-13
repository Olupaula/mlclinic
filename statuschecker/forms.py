from django import forms
from django.forms import Form, ModelForm
from .models import Patient, BreastCancer, Diabetics


class PatientForm(ModelForm):
    # name = forms.CharField(label="Name", max_length=200)
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({
            'id': 'gender',
            # 'disabled':'disabled'
        })


class BreastCancerForm(ModelForm):
    class Meta:
        model = BreastCancer
        exclude = ['patient']

    '''def __init__(self, *args, **kwargs):
        super(BreastCancerForm, self).__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs.update({
            'id': 'md',
            # 'disabled':'disabled'
        })'''


class DiabeticsForm(ModelForm):
    class Meta:
        model = Diabetics
        exclude = ['patient', 'age']
