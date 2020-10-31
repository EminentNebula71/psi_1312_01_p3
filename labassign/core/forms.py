from django import forms
from core.models import Pair, Student

MAX_LENGTH = 128

class PairForm(forms.ModelForm):  
    class Meta:
        model = Pair
        exclude = ('studentBreakRequest', 'validated')


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Student
        fields = ('username',
                  'password',
                  'first_name',
                  'last_name',
                  'gradeTheoryLastYear',
                  'gradeLabLastYear',
                  'labGroup',
                  'theoryGroup',
                  'convalidationGranted')
        