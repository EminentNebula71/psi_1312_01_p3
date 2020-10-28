from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Student(models.AbstractUser):
    labGroup = models.ForeignKey(labGroup, on_delete=models.CASCADE)
    theoryGroup = models.ForeignKey(theoryGroup, on_delete=models.CASCADE)
    first_name = models.CharField(blank=False)
    last_name = models.CharField(blank=False)
    gradeTheoryLastYear = models.FloatField(blank=False)
    gradeLabLastYear = models.FloatField(blank=False)
    convalidationGranted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if(self.gradeTheoryLastYear < 0):
            self.gradeTheoryLastYear = 0

        if(self.gradeLabLastYear < 0):
            self.gradeLabLastYear = 0
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + self.last_name


class Teacher(models.Model):
    first_name = models.CharField(blank=False)
    last_name = models.CharField(blank=False)

    def __str__(self):
        return self.first_name + self.last_name


class TheoryGroup(models.Model):
    groupName = models.CharField(blank=False)
    language = models.CharField(blank=False)

    def __str__(self):
        return self.groupName


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


class LabGroup(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groupName = models.CharField(blank=False)
    language = models.CharField(blank=False)
    schedule = models.CharField(blank=False)
    maxNumberStudents = models.IntegerField(default=1)
    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if(self.maxNumberStudents < 0):
            self.maxNumberStudents = 0

        super(LabGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.groupName


class Pair(models.Model):
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE)
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    studentBreakRequest = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student1 + self.student2




