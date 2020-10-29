from django.shortcuts import render, redirect
from core.models import Pair, Student
from core.forms import PairForm, StudentForm


def create_petition(request):
    form = PairForm()

    if request.method == 'POST':
        form = PairForm(request.POST)

        if form.is_valid():
            try:
                existente = Pair.objects.get(student1=form.student2)
                existente = Pair.objects.get(student2=form.student1)
                existente.validated=True
            except Pair.DoesNotExist:
                pair = form.save()