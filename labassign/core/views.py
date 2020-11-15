from django.shortcuts import render, redirect
from core.models import Pair, Student
from core.forms import PairForm, StudentForm
from django.contrib.auth import authenticate
from django.http import HttpResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('core:home'))

            else:
                return HttpResponse("Your Rango account was disabled")

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details")

    else:
        return render(request, 'core/login.html')

def home(request):
    return render(request, 'core/home.html')

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