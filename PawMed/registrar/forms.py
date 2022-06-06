from django import forms
from .models import Patient
from doctor.models import Doctor, Specialization


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


class AppointmentForm(forms.Form):
    specialization = forms.ChoiceField(
            widget=forms.Select,
            choices=[(specialization.id, specialization.name)
                     for specialization in Specialization.objects.all()],
        )
    doctor = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=[(doctor.id, doctor.name)
                 for doctor in Doctor.objects.all()],
    )
    earliest_date = forms.DateTimeField()
    latest_date = forms.DateTimeField()