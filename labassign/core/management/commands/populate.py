# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate


from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from core.models import (OtherConstraints, Pair, Student,
                         GroupConstraints, TheoryGroup,
                         LabGroup, Teacher)
from django.utils import timezone
import csv
import re

maxNStudents=23

def add_pair(student1, student2):
    try:
        p = Pair.objects.get(student1=Student.objects.get(username=student2),
                             student2=Student.objects.get(username=student1))
        p.validated=True
        p.save()
    except ObjectDoesNotExist:
        p = Pair.objects.get_or_create(student1=Student.objects.get(username=student1),
                                       student2=Student.objects.get(username=student2))


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
#
# Teachers, groups and constraints
# will be hardcoded in this file.
# Students will be read from a cvs file
# last year grade will be obtained from another cvs file
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help="""
        model to  update:
        all -> all models
        teacher
        labgroup
        theorygroup
        groupconstraints
        otherconstrains
        student (require csv file)
        studentgrade (require different csv file,
        update only existing students)
        pair
        """)
        parser.add_argument('studentinfo', type=str, help="""CSV file with student information
        header= NIE, DNI, Apellidos, Nombre, Teoría
        if NIE or DNI == 0 skip this entry and print a warning""")
        parser.add_argument('studentinfolastyear', type=str, help="""CSV file with student information
        header= NIE,DNI,Apellidos,Nombre,Teoría, grade lab, grade the
        if NIE or DNI == 0 skip this entry and print a warning""")

    # handle is another compulsory name, do not change it"
    def handle(self, *args, **kwargs):
        model = kwargs['model']
        cvsStudentFile = kwargs['studentinfo']
        cvsStudentFileGrades = kwargs['studentinfolastyear']
        # clean database
        if model == 'all':
            self.cleanDataBase()
        if model == 'teacher' or model == 'all':
            self.teacher()
        if model == 'labgroup' or model == 'all':
            self.labgroup()
        if model == 'theorygroup' or model == 'all':
            self.theorygroup()
        if model == 'groupconstraints' or model == 'all':
            self.groupconstraints()
        if model == 'otherconstrains' or model == 'all':
            self.otherconstrains()
        if model == 'student' or model == 'all':
            self.student(cvsStudentFile)
        if model == 'studentgrade' or model == 'all':
            self.studentgrade(cvsStudentFileGrades)
        if model == 'pair' or model == 'all':
            self.pair()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        Teacher.objects.all().delete()
        LabGroup.objects.all().delete()
        TheoryGroup.objects.all().delete()
        GroupConstraints.objects.all().delete()
        OtherConstraints.objects.all().delete()
        Student.objects.all().delete()
        Pair.objects.all().delete()


    def teacher(self):
        "create teachers here"
        c = Teacher.objects.get_or_create(first_name="No", last_name="Asignado1")[0]
        c = Teacher.objects.get_or_create(first_name="No", last_name="Asignado4")[0]
        c = Teacher.objects.get_or_create(first_name="Alvaro", last_name="del Val Latorre")[0]
        c = Teacher.objects.get_or_create(first_name="Julia", last_name="Diaz Garcia")[0]
        c = Teacher.objects.get_or_create(first_name="Roberto", last_name="Marabini Ruiz")[0]


    def labgroup(self):
        # Idiomas
        esp = "español/Spanish"
        ing='inglés/English'
        # Horario
        lt='Lunes/Monday 18-20'
        x='Miércoles/Wednesday 18-20'
        v='Viernes/Friday 17-19'
        "add labgroups"
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Roberto"), groupName='1201', language=esp, schedule=x, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(last_name="Asignado1"), groupName='1261', language=esp, schedule=lt, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(last_name="Asignado4"), groupName='1262', language=esp, schedule=x, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(last_name="Asignado4"), groupName='1263', language=esp, schedule=v, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(last_name="Asignado1"), groupName='1271', language=esp, schedule=x, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Alvaro"), groupName='1272', language=esp, schedule=v, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Alvaro"), groupName='1291', language=ing, schedule=lt, maxNumberStudents=maxNStudents)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Julia"), groupName='1292', language=ing, schedule=v, maxNumberStudents=maxNStudents)
        
    def theorygroup(self):
        esp = "español/Spanish"
        ing='inglés/English'
        "add theorygroups"
        t = TheoryGroup.objects.get_or_create(groupName="120", language=esp)
        t = TheoryGroup.objects.get_or_create(groupName="125", language=ing)
        t = TheoryGroup.objects.get_or_create(groupName="126", language=esp)
        t = TheoryGroup.objects.get_or_create(groupName="127", language=esp)
        t = TheoryGroup.objects.get_or_create(groupName="129", language=ing)

    def groupconstraints(self):
        "add group constrints"
        """ Follows which laboratory groups (4th column
            may be choosen by which theory groups (2nd column)
                theoryGroup: 126, labGroup: 1261
                theoryGroup: 126, labGroup: 1262
                theoryGroup: 126, labGroup: 1263
                theoryGroup: 127, labGroup: 1271
                theoryGroup: 127, labGroup: 1272
                theoryGroup: 120, labGroup: 1201
                theoryGroup: 129, labGroup: 1291
                theoryGroup: 125, labGroup: 1292"""
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="126"), labGroup=LabGroup.objects.get(groupName="1261"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="126"), labGroup=LabGroup.objects.get(groupName="1262"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="126"), labGroup=LabGroup.objects.get(groupName="1263"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="127"), labGroup=LabGroup.objects.get(groupName="1271"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="127"), labGroup=LabGroup.objects.get(groupName="1272"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="120"), labGroup=LabGroup.objects.get(groupName="1201"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="129"), labGroup=LabGroup.objects.get(groupName="1291"))
        g = GroupConstraints.objects.get_or_create(theoryGroup=TheoryGroup.objects.get(groupName="125"), labGroup=LabGroup.objects.get(groupName="1292"))
     

    def pair(self):
        "create a few valid pairs"
        # Pareja valida
        add_pair('464353', '460168')
        add_pair('460168', '464353')
        # Peticion no valida
        add_pair('499264', '470075')
        # Peticion triangulo
        add_pair('468608', '447012')
        add_pair('447012', '462402')
        add_pair('462402', '468608')

    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        o = OtherConstraints.objects.get_or_create(minGradeTheoryConv=3, minGradeLabConv=7)[0]
        o.selectGroupStartDate = timezone.now() + timezone.timedelta(days=1)

    def student(self, csvStudentFile):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        with open(csvStudentFile, mode='r') as csv_file:
            info = csv.reader(csv_file, delimiter=',')
            i = 0

            for row in info:
                if i > 0:
                    Student.objects.get_or_create(username = row[0],
                                                  password = row[1],
                                                  last_name = row[2],
                                                  first_name = row[3],
                                                  theoryGroup = TheoryGroup.objects.get(groupName=row[4]))
                i += 1

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría	grade-practicas	gradeteoria
        with open(cvsStudentFileGrades, mode='r') as csv_file:
            info = csv.reader(csv_file, delimiter=',')
            i = 0

            for row in info:
                if i > 0:
                    try :
                        s = Student.objects.get(username=row[0])
                        s.delete()
                        Student.objects.get_or_create(username = row[0],
                                                    password = row[1],
                                                    last_name = row[2],
                                                    first_name = row[3],
                                                    theoryGroup = TheoryGroup.objects.get(groupName=row[4]),
                                                    gradeLabLastYear=float(row[5]),
                                                    gradeTheoryLastYear=float(row[6]))
                    except ObjectDoesNotExist:
                        Student.objects.get_or_create(username = row[0],
                                                    password = row[1],
                                                    last_name = row[2],
                                                    first_name = row[3],
                                                    theoryGroup = TheoryGroup.objects.get(groupName=row[4]),
                                                    gradeLabLastYear=float(row[5]),
                                                    gradeTheoryLastYear=float(row[6]),
                                                    labGroup = LabGroup.objects.get(groupName='1261')) #CUIDADO HAY QUE ARREGLAR ESTO
   
                i += 1
