from django.contrib import admin
from exam.models import Category, Question, TestResult, Feedback


# CategoryAdmin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("name",)


# QuestionAdmin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "difficulty", "question_text", "correct_option",)

    list_filter = ("category", "difficulty",)

    search_fields = ("question_text", "category__name",)

    ordering = ("category", "difficulty")


# TestResultAdmin
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "category", "difficulty_level", "percentage", "date_attempted",)

    list_filter = ("category", "difficulty_level", "date_attempted",)

    search_fields = ("user__username", "category__name",)

    ordering = ("-date_attempted",)


# FeedbackAdmin
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # id, name, email, rating, message, created_at
    list_display = ("id", "name", "rating", "created_at",)

    list_filter = ("rating", "created_at",)

    search_fields = ("name", "message",)

    ordering = ("-created_at",)





    