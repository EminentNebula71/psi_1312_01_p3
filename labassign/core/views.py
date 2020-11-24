from django.shortcuts import render, redirect
from core.models import (Pair, Student,
                         OtherConstraints,
                         GroupConstraints,
                         LabGroup)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def home(request):
    """
    Función que retorna la vista en la web de la página de inicio,
        con la información necesaria para visualizar la información
        del estudiante.
    Autor: Elena Diego
    """
    pairs = Pair.objects.all()
    context_dict = {}
    context_dict['pairs'] = pairs
    return render(request, 'core/home.html', context_dict)


@login_required
def convalidation(request):
    """
    Función que procesa la convalidación de las prácticas de un
        estudiante en base a las condiciones dadas.
    Autor: Ángel Bernal
    """
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
    """
    Función que, si no viene del formulario de elegir pareja,
        devuelve la vista de la página web applypair en la que
        se visualiza las posibles parejas entre las que el usuario
        puede elegir.
        Si viene desde el formulario (con el request.method='POST')
        se procesa la petición de la pareja, creandola en el caso de
        que solo el estudiante1 la haya pedido y validándola si es el
        estudiante2 de la pareja la que lo solicita.
    Autor: Elena Diego
    """
    if request.method == 'POST':
        if request.user.es_pareja == 1:
            students = Student.objects.all().exclude(es_pareja_validada=1)
            students_final = students.exclude(username=request.user.username)
            pareja_mismo_usuario = "User has already selected a pair"
            context_dict = {}
            context_dict['students'] = students_final
            context_dict['pareja_mismo_usuario'] = pareja_mismo_usuario
            return render(request, 'core/applypair.html', context_dict)

        user1 = request.user
        user2_id = request.POST.get("colegas")
        user2 = Student.objects.get(id=user2_id)
        try:
            pareja = Pair.objects.get(student1=user2, student2=user1)
            pareja.validated = True
            pareja.save()
            user1.es_pareja = 1
            user1.es_pareja_validada = 1
            user1.save()
            user2.es_pareja_validada = 1
            user2.save()

        except ObjectDoesNotExist:
            Pair.objects.create(student1=user1, student2=user2)
            user1.es_pareja = 1
            user1.save()

        return redirect(reverse('core:home'))

    if request.user.es_pareja == 1:
        return redirect(reverse('core:home'))

    students = Student.objects.all().exclude(es_pareja_validada=1)
    students_final = students.exclude(username=request.user.username)
    context_dict = {}
    context_dict['students'] = students_final
    return render(request, 'core/applypair.html', context_dict)


@login_required
def elegir_grupo(request):
    """
    Función que, si no viene del formulario de elegir grupo,
        devuelve la vista de la página web elegir_grupo en la que
        se visualiza los posibles grupos de laboratorio entre los
        que el usuario puede elegir.
        Si viene desde el formulario (con el request.method='POST')
        se procesa la petición del grupo, añadiendo al estudiante si no
        tiene pareja y hay espacio o añadiendo también a su pareja siempre que
        haya dos espacios libres en el grupo.
    Autor: Ángel Bernal
    """
    if request.method == 'POST':
        user1 = request.user
        grupo_id = request.POST.get("grupos")
        grupo = LabGroup.objects.get(id=grupo_id)
        if(user1.es_pareja_validada == 1):
            try:
                pair = Pair.objects.get(student1=user1, validated=True)
                user2 = pair.student2
            except ObjectDoesNotExist:
                pair = Pair.objects.get(student2=user1, validated=True)
                user2 = pair.student1
            finally:
                if((grupo.maxNumberStudents-grupo.counter) >= 2):
                    user1.labGroup = grupo
                    user2.labGroup = grupo
            user1.esta_grupo = 1
            user1.save()
            user2.esta_grupo = 1
            user2.save()
            grupo.counter += 2
            grupo.save()

        elif(grupo.maxNumberStudents > grupo.counter):
            user1.labGroup = grupo
            user1.esta_grupo = 1
            user1.save()
            grupo.counter += 1
            grupo.save()

        return redirect(reverse('core:home'))

    grupo_student = request.user.theoryGroup
    grupos_lab = GroupConstraints.objects.filter(theoryGroup=grupo_student)
    print(grupos_lab)
    for g in grupos_lab:
        if g.labGroup.counter >= g.labGroup.maxNumberStudents:
            grupos_lab = grupos_lab.exclude(id=g.id)
    aux = OtherConstraints.objects.all().first().selectGroupStartDate
    if timezone.now() < aux:
        valido = 0
    else:
        valido = 1
    context_dict = {}
    context_dict['grupos_lab'] = grupos_lab
    context_dict['valido'] = valido
    return render(request, 'core/elegir_grupo.html', context_dict)
