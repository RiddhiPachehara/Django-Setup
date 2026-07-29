from django.contrib import admin
from .models import School, Classroom, Student, Teacher, Library

admin.site.register(School)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Library)