from core.models import (OtherConstraints,
                         Pair, Student,
                         TheoryGroup)
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from core.management.commands.populate import Command
from django.utils import timezone


class test_query_class(TestCase):

    def setUp(self):
        self.client = Client()
        # load Command class from populate
        c = Command()
        # execute populate
        c.handle(model='all', studentinfo='19-edat_psi.csv',
                 studentinfolastyear='19-edat_2_psi.csv')

    def test_query(self):
        try:
            user_1000 = Student.objects.get(id=1000)
        except ObjectDoesNotExist:
            user_1000 = Student.objects.create(
                id=1000,
                username=516382,
                password=123456789,
                last_name="Almodóvar",
                first_name="Pedro",
                theoryGroup=TheoryGroup.objects.get(groupName="126"))

        try:
            user_1001 = Student.objects.get(id=1001)
        except ObjectDoesNotExist:
            user_1000 = Student.objects.create(
                id=1001,
                username=854621,
                password=987654321,
                last_name="Mota",
                first_name="José",
                theoryGroup=TheoryGroup.objects.get(groupName="126"))

        Pair.objects.create(
                student1=user_1000,
                student2=user_1001)

        parejas = Pair.objects.filter(student1=user_1000).all()
        print(parejas)
        parejas.all().validated = True
        print(parejas)
        for p in parejas.all():
            p.save()

        OtherConstraints.objects.create(
            selectGroupStartDate=(timezone.now()+timezone.timedelta(days=1)))
        cons = OtherConstraints.objects.all()

        if cons[0].selectGroupStartDate > timezone.now():
            print("Está en el futuro.")
        else:
            print("Está en el pasado.")
