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
from django.contrib.auth.hashers import make_password

maxNStudents = 23


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
        Teacher.objects.get_or_create(
            id=1,
            first_name="No",
            last_name="Asignado1")[0]
        Teacher.objects.get_or_create(
            id=2,
            first_name="No",
            last_name="Asignado4")[0]
        Teacher.objects.get_or_create(
            id=3,
            first_name="Alvaro",
            last_name="del Val Latorre")[0]
        Teacher.objects.get_or_create(
            id=4,
            first_name="Julia",
            last_name="Diaz Garcia")[0]
        Teacher.objects.get_or_create(
            id=5,
            first_name="Roberto",
            last_name="Marabini Ruiz")[0]

    def labgroup(self):
        # Idiomas
        esp = "español/Spanish"
        ing = 'inglés/English'
        # Horario
        lt = 'Lunes/Monday 18-20'
        x = 'Miércoles/Wednesday 18-20'
        v = 'Viernes/Friday 17-19'
        "add labgroups"
        LabGroup.objects.get_or_create(
            id=1201,
            teacher=Teacher.objects.get(first_name="Roberto"),
            groupName='1201',
            language=esp,
            schedule=x,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1261,
            teacher=Teacher.objects.get(last_name="Asignado1"),
            groupName='1261',
            language=esp,
            schedule=lt,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1262,
            teacher=Teacher.objects.get(last_name="Asignado4"),
            groupName='1262',
            language=esp,
            schedule=x,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1263,
            teacher=Teacher.objects.get(last_name="Asignado4"),
            groupName='1263',
            language=esp,
            schedule=v,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1271,
            teacher=Teacher.objects.get(last_name="Asignado1"),
            groupName='1271',
            language=esp,
            schedule=x,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1272,
            teacher=Teacher.objects.get(first_name="Alvaro"),
            groupName='1272',
            language=esp,
            schedule=v,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1291,
            teacher=Teacher.objects.get(first_name="Alvaro"),
            groupName='1291',
            language=ing,
            schedule=lt,
            maxNumberStudents=maxNStudents)[0]
        LabGroup.objects.get_or_create(
            id=1292,
            teacher=Teacher.objects.get(first_name="Julia"),
            groupName='1292',
            language=ing,
            schedule=v,
            maxNumberStudents=maxNStudents)[0]

    def theorygroup(self):
        esp = "español/Spanish"
        ing = 'inglés/English'
        "add theorygroups"
        TheoryGroup.objects.get_or_create(
            id=120,
            groupName="120",
            language=esp)[0]
        TheoryGroup.objects.get_or_create(
            id=125,
            groupName="125",
            language=ing)[0]
        TheoryGroup.objects.get_or_create(
            id=126,
            groupName="126",
            language=esp)[0]
        TheoryGroup.objects.get_or_create(
            id=127,
            groupName="127",
            language=esp)[0]
        TheoryGroup.objects.get_or_create(
            id=129,
            groupName="129",
            language=ing)[0]

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
        GroupConstraints.objects.get_or_create(
            id=1261,
            theoryGroup=TheoryGroup.objects.get(id=126),
            labGroup=LabGroup.objects.get(groupName="1261"))[0]
        GroupConstraints.objects.get_or_create(
            id=1262,
            theoryGroup=TheoryGroup.objects.get(groupName="126"),
            labGroup=LabGroup.objects.get(groupName="1262"))[0]
        GroupConstraints.objects.get_or_create(
            id=1263,
            theoryGroup=TheoryGroup.objects.get(groupName="126"),
            labGroup=LabGroup.objects.get(groupName="1263"))[0]
        GroupConstraints.objects.get_or_create(
            id=1271,
            theoryGroup=TheoryGroup.objects.get(groupName="127"),
            labGroup=LabGroup.objects.get(groupName="1271"))[0]
        GroupConstraints.objects.get_or_create(
            id=1272,
            theoryGroup=TheoryGroup.objects.get(groupName="127"),
            labGroup=LabGroup.objects.get(groupName="1272"))[0]
        GroupConstraints.objects.get_or_create(
            id=1201,
            theoryGroup=TheoryGroup.objects.get(groupName="120"),
            labGroup=LabGroup.objects.get(groupName="1201"))[0]
        GroupConstraints.objects.get_or_create(
            id=1291,
            theoryGroup=TheoryGroup.objects.get(groupName="129"),
            labGroup=LabGroup.objects.get(groupName="1291"))[0]
        GroupConstraints.objects.get_or_create(
            id=1292,
            theoryGroup=TheoryGroup.objects.get(groupName="125"),
            labGroup=LabGroup.objects.get(groupName="1292"))[0]

    def pair(self):
        "create a few valid pairs"
        pairD = {}
        pairD[1000] = {'student2': 1100, 'validated': False}
        pairD[1001] = {'student2': 1101, 'validated': False}
        pairD[1010] = {'student2': 1110, 'validated': True}
        pairD[1011] = {'student2': 1111, 'validated': True}
        pairD[1012] = {'student2': 1112, 'validated': True}

        for key, value in pairD.items():
            Pair.objects.create(
                student1=Student.objects.get(id=key),
                student2=Student.objects.get(id=value['student2']),
                validated=value['validated'])                
            student=Student.objects.get(id=key)
            student.es_pareja=1
            if(value['validated']==True):
                student.es_pareja_validada=1
            student.save()
            student=Student.objects.get(id=value['student2'])
            student.es_pareja=1
            if(value['validated']==True):
                student.es_pareja_validada=1
            student.save()


    def otherconstrains(self):
        """create a single object here with staarting dates
        and maximum and minimum convalidation grades"""
        """ Use the following values:
        selectGroupStartDate = now + 1 day,
        minGradeTheoryConv = 3,
        minGradeLabConv = 7
        """
        o = OtherConstraints.objects.get_or_create(
            minGradeTheoryConv=3, minGradeLabConv=7)[0]
        o.selectGroupStartDate = timezone.now() + timezone.timedelta(days=1)
        o.save()

    def student(self, csvStudentFile):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        with open(csvStudentFile, mode='r') as csv_file:
            info = csv.reader(csv_file, delimiter=',')

            for index, row in enumerate(info):
                if index > 0:
                    Student.objects.create_user(
                        id=index+999,
                        username=row[0],
                        password=row[1],
                        last_name=row[2],
                        first_name=row[3],
                        theoryGroup=TheoryGroup.objects.get(
                            groupName=row[4]))

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure
        # NIE
        # DNI
        # Apellidos
        # Nombre
        # group-Teoría
        # grade-practicas
        # gradeteoria
        with open(cvsStudentFileGrades, mode='r') as csv_file:
            info = csv.reader(csv_file, delimiter=',')

            for index, row in enumerate(info):
                if index > 0:
                    try:
                        Student.objects.filter(
                            username=row[0]).update(
                                gradeLabLastYear=float(row[5]),
                                gradeTheoryLastYear=float(row[6]))
                    except ObjectDoesNotExist:
                        print("Grade for non existing users.")
