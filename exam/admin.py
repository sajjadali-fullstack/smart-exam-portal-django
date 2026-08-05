from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Question, TestResult, Feedback

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(TestResult)
admin.site.register(Feedback)