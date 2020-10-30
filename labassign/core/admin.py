from django.contrib import admin
from core.models import Teacher, LabGroup, TheoryGroup, OtherConstraints, GroupConstraints, Student, Pair

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'gradeTheoryLastYear')
class OtherConstraintsAdmin(admin.ModelAdmin):
    list_display = ('selectGroupStartDate', 'minGradeTheoryConv', 'minGradeLabConv')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')

class LabGroupAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'groupName', 'language', 'schedule', 'maxNumberStudents', 'counter')

admin.site.register(Student)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TheoryGroup)
admin.site.register(OtherConstraints, OtherConstraintsAdmin)
admin.site.register(GroupConstraints)
admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(Pair)
