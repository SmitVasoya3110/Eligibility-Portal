from django.contrib import admin
from .models import Exam, College,  Question, Option

# Register your models here.
admin.site.register(College)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Option)