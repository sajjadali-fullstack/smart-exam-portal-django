from django.db import models
from django.db import models
from django.contrib.auth.models import User


# Create your models / SQL Tables here 👇.

# Exam Category (Python, Accounts, React, etc.)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name




# Question Bank with Difficulty and Category Link
class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    # question_text = models.CharField(max_length=500)
    question_text = models.TextField(max_length=900)

    option1 = models.TextField(max_length=900)
    option2 = models.TextField(max_length=900)
    option3 = models.TextField(max_length=900)
    option4 = models.TextField(max_length=900)
    
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')
    
    # 💡 Naya Feature: Train mein revision ke waqt ya galat answer hone par kaam aayega
    explanation = models.TextField(blank=True, null=True, help_text="Sawal ka sahi jawab kyun hai, yahan vistaar se likhein.")

    def __str__(self):
        return f"[{self.category.name} - {self.difficulty}] {self.question_text[:30]}"





# 3. Test Result / Leaderboard Entries
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    percentage = models.FloatField()
    time_taken = models.IntegerField() # Total seconds taken to finish the exam (e.g., 240 seconds)
    difficulty_level = models.CharField(max_length=10)
    date_attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.difficulty_level}) - {self.percentage}%"





# Feedback Form
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    rating = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ⭐ {self.rating}"