from core.models import (OtherConstraints, Pair, Student, GroupConstraints, TheoryGroup, LabGroup, Teacher)
from django.test import TestCase

class test_query_class(TestCase):
    def add_pair(student1, student2):
        p = Pair.objects.get(student1=student1, student2=student2)
        

    def test_query(self):
        user_1000=Student.objects.get_or_create(id=1000,
                                                username = 516382,
                                                password = 123456789,
                                                last_name = "Almodóvar",
                                                first_name = "Pedro",
                                                theoryGroup = TheoryGroup.objects.get(groupName="126"))

        user_1001=Student.objects.get_or_create(id=1001,
                                                username = 854621,
                                                password = 987654321,
                                                last_name = "Mota",
                                                first_name = "José",
                                                theoryGroup = TheoryGroup.objects.get(groupName="126"))
        add_pair(user_1000, user_1001)
        parejas = Pair.objects.get(student1=user_1000).all()
        print(parejas)
        parejas.all().validated=True
        parejas.all().save()
