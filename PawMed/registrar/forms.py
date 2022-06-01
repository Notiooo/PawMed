from django import forms
from .models import Patient


class PatientBoardForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['personid', 'name', 'surname']

    def find_patient(self):
        return Patient.objects.filter(name=self.cleaned_data['name'], surname=self.cleaned_data['surname'], personid=self.cleaned_data['personid'])

    def clean(self):
        if len(self.find_patient()) != 1:
            raise forms.ValidationError('User not found')
        return super().clean()
