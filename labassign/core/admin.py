from django.contrib import admin
from core.models import Teacher, LabGroup, TheoryGroup, OtherConstraints, GroupConstraints, Student, Pair

class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)
    ordering = ('last_name', 'first_name',)

class OtherConstraintsAdmin(admin.ModelAdmin):
    list_display = ('selectGroupStartDate', 'minGradeTheoryConv', 'minGradeLabConv')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name',)

class LabGroupAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'groupName', 'language', 'schedule', 'maxNumberStudents', 'counter')
    ordering = ('groupName',)

class TheoryGroupAdmin(admin.ModelAdmin):
    ordering = ('groupName',)

class GroupConstraintsAdmin(admin.ModelAdmin):
    ordering = ('theoryGroup', 'labGroup',)
    
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TheoryGroup, TheoryGroupAdmin)
admin.site.register(OtherConstraints, OtherConstraintsAdmin)
admin.site.register(GroupConstraints, GroupConstraintsAdmin)
admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(Pair)
