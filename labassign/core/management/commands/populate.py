# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate


from django.core.management.base import BaseCommand
from core.models import (OtherConstraints, Pair, Student,
                         GroupConstraints, TheoryGroup,
                         LabGroup, Teacher)
from django.utils import timezone
import csv


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
        c = Teacher.objects.get_or_create(first_name="Carlos", last_name="Santa Cruz")[0]
        c = Teacher.objects.get_or_create(first_name="Francisco", last_name="de Borja")[0]
        c = Teacher.objects.get_or_create(first_name="Pablo", last_name="Castells")[0]
        c = Teacher.objects.get_or_create(first_name="Roberto", last_name="Marabini")[0]
        c = Teacher.objects.get_or_create(first_name="Álvaro", last_name="del Val")[0]

    def labgroup(self):
        "add labgroups"
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Álvaro"), groupName='1263', language='Español', schedule='17 a 19 los viernes', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Pablo"), groupName='1261', language='Español', schedule='18 a 20 los lunes', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Carlos"), groupName='1262', language='Español', schedule='18 a 20 los miércoles', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Francisco"), groupName='1271', language='Español', schedule='18 a 20 los miércoles', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Carlos"), groupName='1272', language='Español', schedule='17 a 19 los viernes', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Álvaro"), groupName='1273', language='Español', schedule='17 a 19 los viernes', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Roberto"), groupName='1291', language='Inglés', schedule='18 a 20 los lunes', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Roberto"), groupName='1292', language='Inglés', schedule='17 a 19 los viernes', maxNumberStudents=30)
        l = LabGroup.objects.get_or_create(teacher=Teacher.objects.get(first_name="Roberto"), groupName='1201', language='Inglés', schedule='17 a 19 los viernes', maxNumberStudents=30)
        
    def theorygroup(self):
        "add theorygroups"
        t = TheoryGroup.objects.get_or_create(groupName="126", language="Español")
        t = TheoryGroup.objects.get_or_create(groupName="127", language="Español")
        t = TheoryGroup.objects.get_or_create(groupName="120", language="Español")
        t = TheoryGroup.objects.get_or_create(groupName="125", language="Español")
        t = TheoryGroup.objects.get_or_create(groupName="129", language="Inglés")

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
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="126"), labGroup=LabGroup.objects.get(groupName="1261"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="126"), labGroup=LabGroup.objects.get(groupName="1262"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="126"), labGroup=LabGroup.objects.get(groupName="1263"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="127"), labGroup=LabGroup.objects.get(groupName="1271"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="127"), labGroup=LabGroup.objects.get(groupName="1272"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="120"), labGroup=LabGroup.objects.get(groupName="1201"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="129"), labGroup=LabGroup.objects.get(groupName="1291"))
        g = GroupConstraints.objects.get_or_create(TheoryGroup=TheoryGroup.objects.get(groupName="125"), labGroup=LabGroup.objects.get(groupName="1292"))
     


    def pair(self):
        "create a few valid pairs"
        # remove pass and ADD CODE HERE
        pass

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
        # remove pass and ADD CODE HERE
        pass

    def studentgrade(self, cvsStudentFileGrades):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría	grade-practicas	gradeteoria
        # remove pass and ADD CODE HERE
        pass
