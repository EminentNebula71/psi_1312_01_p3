from django.shortcuts import render, redirect
from core.models import Pair, Student, OtherConstraints
from core.forms import PairForm, StudentForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def home(request):
    pairs=Pair.objects.all()
    context_dict = {}
    context_dict['pairs'] = pairs
    return render(request, 'core/home.html', context_dict)

def create_petition(request):
    form = PairForm()

    if request.method == 'POST':
        form = PairForm(request.POST)

        if form.is_valid():
            try:
                existente1 = Pair.objects.get(student1=form.student2)
                existente2 = Pair.objects.get(student2=form.student1)
                if (existente1==existente2):
                    existente1.validated=True
            except Pair.DoesNotExist:
                pair = form.save()

        else:
            print(form.errors)

    return

@login_required
def convalidation(request):
    username = request.POST.get('username')

    student1 = Student.objects.get(username=username)
    st_theory = student1.gradeTheoryLastYear
    st_lab = student1.gradeLabLastYear
    print(st_lab)
    # ESTO PUEDE PETAR
    ot = OtherConstraints.objects.all().first()
    min_theory = ot.minGradeTheoryConv
    min_lab = ot.minGradeLabConv
    print(min_lab)
    if st_theory > min_theory and st_lab > min_lab:
        print("Cambia")
        student1.convalidationGranted = True
        student1.save()
    return redirect(reverse('core:home'))
