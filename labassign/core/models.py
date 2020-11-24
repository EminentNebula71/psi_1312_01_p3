from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.functions import Upper


class Teacher(models.Model):
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)

    class Meta:
        ordering = [Upper('last_name'), 'first_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class LabGroup(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groupName = models.CharField(blank=False, max_length=50, unique=True)
    language = models.CharField(blank=False, max_length=50)
    schedule = models.CharField(blank=False, max_length=150)
    maxNumberStudents = models.IntegerField(default=1)
    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if(self.maxNumberStudents < 0):
            self.maxNumberStudents = 0

        super(LabGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.groupName


class TheoryGroup(models.Model):
    groupName = models.CharField(blank=False, max_length=50, unique=True)
    language = models.CharField(blank=False, max_length=50)

    class Meta:
        ordering = ['groupName']

    def __str__(self):
        return self.groupName


class Student(AbstractUser):
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE, null=True)
    theoryGroup = models.ForeignKey(
        TheoryGroup,
        on_delete=models.CASCADE,
        null=True)
    gradeTheoryLastYear = models.FloatField(default=0.0)
    gradeLabLastYear = models.FloatField(default=0.0)
    convalidationGranted = models.BooleanField(default=False)
    # Flag para comprobar que el estudiante ha seleccionado una pareja
    es_pareja = models.IntegerField(default=0)
    # Flag para comprobar que el estudiante está en una pareja validada
    es_pareja_validada = models.IntegerField(default=0)
    # Flag para comprobar que el estudiante está en un grupo de laboratorio
    esta_grupo = models.IntegerField(default=0)

    class Meta:
        ordering = [Upper('last_name'), 'first_name']

    def save(self, *args, **kwargs):
        if(self.gradeTheoryLastYear < 0.0):
            self.gradeTheoryLastYear = 0.0

        if(self.gradeLabLastYear < 0):
            self.gradeLabLastYear = 0
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class OtherConstraints(models.Model):
    selectGroupStartDate = models.DateTimeField(default=timezone.now)
    minGradeTheoryConv = models.FloatField(blank=True, default=0.0)
    minGradeLabConv = models.FloatField(blank=True, default=0.0)

    def save(self, *args, **kwargs):
        if (self.minGradeTheoryConv < 0.0):
            self.minGradeTheoryConv = 0
        if (self.minGradeLabConv < 0.0):
            self.minGradeLabConv = 0
        if(self.selectGroupStartDate < timezone.now()):
            self.selectGroupStartDate = timezone.now()
        super(OtherConstraints, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.minGradeLabConv) + str(self.minGradeTheoryConv)


class GroupConstraints(models.Model):
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)

    class Meta:
        ordering = ['labGroup', 'theoryGroup']

    def __str__(self):
        return self.theoryGroup.groupName + ', ' + self.labGroup.groupName


class Pair(models.Model):
    student1 = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='student1')
    student2 = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='student2')
    validated = models.BooleanField(default=False)
    studentBreakRequest = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True)

    def __str__(self):
        return "\nstudent1 --> (%d) %s, %s \n" \
               "student2 --> (%d) %s, %s. Val =%r\n" % \
               (self.student1.id, self.student1.last_name,
                self.student1.first_name, self.student2.id,
                self.student2.last_name, self.student2.first_name,
                self.validated)

    class Meta:
        ordering = ['student1__id', 'student2__id']
