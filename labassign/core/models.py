from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

class Teacher(models.Model):
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.first_name + self.last_name


class LabGroup(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groupName = models.CharField(blank=False, max_length=50)
    language = models.CharField(blank=False, max_length=50)
    schedule = models.CharField(blank=False, max_length=50)
    maxNumberStudents = models.IntegerField(default=1)
    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if(self.maxNumberStudents < 0):
            self.maxNumberStudents = 0

        super(LabGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.groupName


class TheoryGroup(models.Model):
    groupName = models.CharField(blank=False, max_length=50)
    language = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.groupName


class Student(AbstractBaseUser):
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    gradeTheoryLastYear = models.FloatField(default=0)
    gradeLabLastYear = models.FloatField(default=0)
    convalidationGranted = models.BooleanField(default=False)
    username = models.CharField(blank=False, max_length=50, unique=True, default='default')
    password = models.CharField(blank=False, max_length=50)
    
    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if(self.gradeTheoryLastYear < 0.0):
            self.gradeTheoryLastYear = 0.0

        if(self.gradeLabLastYear < 0):
            self.gradeLabLastYear = 0
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + self.last_name


class OtherConstraints(models.Model):
    selectGroupStartDate = models.DateTimeField(default=timezone.now())
    minGradeTheoryConv = models.FloatField(blank=False)
    minGradeLabConv = models.FloatField(blank=False)

    def save(self, *args, **kwargs):
        if (self.minGradeTheoryConv < 0):
            self.minGradeTheoryConv = 0
        if (self.minGradeLabConv < 0):
            self.minGradeLabConv = 0
        if(self.selectGroupStartDate < timezone.now()):
            self.selectGroupStartDate = timezone.now()
        super(OtherConstraints, self).save(*args, **kwargs)

    def __str__(self):
        return self.id


class GroupConstraints(models.Model):
    TheoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Pair(models.Model):
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student1')
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student2')
    validated = models.BooleanField(default=False)
    studentBreakRequest = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student1 + self.student2
