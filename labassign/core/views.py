from django.shortcuts import render, redirect
from core.models import Pair, Student, OtherConstraints, GroupConstraints, LabGroup
from core.forms import PairForm, StudentForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


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
    st_theory = request.user.gradeTheoryLastYear
    st_lab = request.user.gradeLabLastYear

    ot = OtherConstraints.objects.all().first()
    min_theory = ot.minGradeTheoryConv
    min_lab = ot.minGradeLabConv

    if st_theory >= min_theory and st_lab >= min_lab:
        request.user.convalidationGranted = True
        request.user.save()

    return render(request, 'core/convalidation.html')


@login_required
def applypair(request):
    students = Student.objects.all().exclude(es_pareja_validada=1)
    students_final = students.exclude(username=request.user.username)
    context_dict = {}
    context_dict['students'] = students_final
    return render(request, 'core/applypair.html', context_dict)


def confirmar_pareja(request):
    user1=request.user
    user2_id=request.POST.get("colegas")
    user2=Student.objects.get(id=user2_id)
    try:
        pareja=Pair.objects.get(student1=user2, student2=user1)
        pareja.validated=True
        pareja.save()
        user1.es_pareja=1
        user1.es_pareja_validada=1
        user1.save()
        user2.es_pareja_validada=1
        user2.save()

    except ObjectDoesNotExist:
        Pair.objects.create(student1=user1, student2=user2)
        user1.es_pareja=1
        user1.save()
        
    return redirect(reverse('core:home'))


@login_required
def elegir_grupo(request):
    grupo_student = request.user.theoryGroup
    grupos_lab = GroupConstraints.objects.filter(theoryGroup=grupo_student)
    print(grupos_lab)
    for g in grupos_lab:
        if g.labGroup.counter >= g.labGroup.maxNumberStudents:
            grupos_lab = grupos_lab.exclude(id=g.id)
    if timezone.now() < OtherConstraints.objects.all().first().selectGroupStartDate:
        valido=0
    else:
        valido=1

    context_dict = {}
    context_dict['grupos_lab'] = grupos_lab
    context_dict['valido'] = valido
    return render(request, 'core/elegir_grupo.html', context_dict)


def confirmar_grupo(request):
    user1=request.user
    grupo_id=request.POST.get("grupos")
    grupo=LabGroup.objects.get(id=grupo_id)
    if(user1.es_pareja_validada==1):
        try:
            pair = Pair.objects.get(student1=user1, validated=True)
        except ObjectDoesNotExist:
            pair = Pair.objects.get(student2=user1, validated=True)
        finally:
            user2 = pair.student2
            if((grupo.maxNumberStudents-grupo.counter)>=2):
                user1.labGroup=grupo
        user1.esta_grupo=1
        user1.save()
        user2.esta_grupo=1
        user2.save()
        grupo.counter+=2
        grupo.save()

    elif(grupo.maxNumberStudents > grupo.counter):
        user1.labGroup=grupo
        user1.esta_grupo=1
        user1.save()
        grupo.counter+=1
        grupo.save()
    
    return redirect(reverse('core:home'))