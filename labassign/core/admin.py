from django.contrib import admin
from core.models import Teacher, LabGroup, TheoryGroup, OtherConstraints, GroupConstraints, Student, Pair

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'gradeTheoryLastYear')


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TheoryGroup)
admin.site.register(OtherConstraints)
admin.site.register(GroupConstraints)
admin.site.register(LabGroup)
admin.site.register(Pair)
