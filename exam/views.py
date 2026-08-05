from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Question, TestResult
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

from django.http import JsonResponse
import json

from exam.models import Feedback
from .forms import FeedbackForm
from django.contrib import messages


# Create your views / business logic here 👇.






# HomePage View: Saari Categories list karega
def homepage(request):
    # categories = Category.objects.all()
    # return render(request, 'exam/homepage.html', {'categories': categories})
    context = {
        "categories": Category.objects.all(),
        "users_count": User.objects.count(),
        "questions_count": Question.objects.count(),
        "attempts_count": TestResult.objects.count(),
        "categories_count": Category.objects.count(),
    }
    return render(request, "exam/homepage.html", context)




# QuizPage View : Category aur Difficulty ke basis par test load karega
@login_required
@never_cache
def take_quiz(request, category_name, difficulty):
    category = get_object_or_404(Category, name__iexact=category_name)
    questions = Question.objects.filter(category=category, difficulty=difficulty)

    # Agar is category + difficulty ke questions hi nahi hain
    # Minimum 9 questions hone chahiye
    if questions.count() < 9:
        return render(request, 'exam/coming_soon.html', {
            'category': category,
            'difficulty': difficulty,
            'available': questions.count()
        })

    if request.method == 'POST':
        correct = 0
        total = questions.count()
        
        # User ke answers ko session mein temporary store karenge review page ke liye
        user_answers = {}
        for q in questions:
            selected_option = request.POST.get(f'q_{q.id}')
            user_answers[str(q.id)] = int(selected_option) if selected_option else None
            if selected_option and int(selected_option) == q.correct_option:
                correct += 1
                
        percentage = (correct / total) * 100 if total > 0 else 0
        
        # Performance Save karo aur object ko ek variable mein le lo
        result = TestResult.objects.create(
            user=request.user,
            category=category,
            total_questions=total,
            correct_answers=correct,
            percentage=round(percentage, 2),
            difficulty_level=difficulty,
            time_taken=120  # Temporary hardcoded
        )
        
        # Session mein is specific result ID ke answers save kar do
        request.session[f'answers_{result.id}'] = user_answers
        
        # 🎯 Wapas Dashboard par bhejo jaisa pehle hota tha!
        return redirect('dashboard')
        
    return render(request, 'exam/quiz.html', {
        'questions': questions, 
        'category': category, 
        'difficulty': difficulty
    })




#  Quiz Review View: Jo Dashboard se click karne par Review page kholega
@login_required
def quiz_review_view(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    questions = Question.objects.filter(category=result.category, difficulty=result.difficulty_level)
    
    # Session se user ke answers nikalna
    saved_answers = request.session.get(f'answers_{result.id}', {})
    
    review_data = []
    for q in questions:
        selected_int = saved_answers.get(str(q.id))
        is_correct = (selected_int == q.correct_option)
        
        review_data.append({
            'question': q,
            'selected': selected_int,
            'is_correct': is_correct,
            'correct_text': getattr(q, f'option{q.correct_option}'),
            'selected_text': getattr(q, f'option{selected_int}') if selected_int else "Attempt Nahi Kiya"
        })
        
    return render(request, 'exam/quiz_review.html', {
        'review_data': review_data,
        'result': result
    })



# Dashboard / Leaderboard View
# def dashboard(request):
#     # Top 10 highest marks scorers globally
#     top_performers = TestResult.objects.order_by('-percentage',  'time_taken')

#     top_three = top_performers[:3]
#     others = top_performers[3:]

#     return render(request, 'exam/dashboard.html', {'top_three': top_three, 'others': others,})
def dashboard(request):
    top_performers = TestResult.objects.order_by('-percentage', 'time_taken', 'date_attempted')

    return render(request, 'exam/dashboard.html', {
        'top_performers': top_performers,
        'top_three': top_performers[:3],
    })



# Register View: User Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Register hote hi user automatic login ho jayega
            messages.success(request, "Registration successful!")
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'exam/register.html', {'form': form})




# Python Query for Category-Wise No.1 Winner
def get_category_winner(category_id):
    winner = TestResult.objects.filter(category_id=category_id)\
                       .order_by('-percentage', 'time_taken')\
                       .first() # Sirf pehla banda (Rank 1) nikalega
    return winner



# Interactive Quiz API View: For JavaScript
@login_required
def interactive_quiz_api(request, category_name, difficulty):
    category = get_object_or_404(Category, name__iexact=category_name)
    questions = Question.objects.filter(category=category, difficulty=difficulty)
    
    # Questions ko JSON formats mein badalna taaki JavaScript handle kar sake
    questions_data = []
    for q in questions:
        questions_data.append({
            'id': q.id,
            'question_text': q.question_text,
            'options': [q.option1, q.option2, q.option3, q.option4],
            'correct_option': q.correct_option,
            'explanation': q.explanation if q.explanation else "Sahi jawab database mein update nahi kiya gaya hai."
        })
        
    return JsonResponse({
        'category': category.name,
        'difficulty': difficulty,
        'questions': questions_data
    })




# About View
def about_view(request):
    return render(request, 'exam/about.html')


# Feedback View
@login_required
def feedback_view(request):

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Thank you for your valuable feedback!")
            return redirect("reviews")

    else:
        form = FeedbackForm()

    return render(request, "exam/feedback.html", {
        "form": form
    })




# Reviews View
# @login_required
def reviews_view(request):

    reviews = Feedback.objects.order_by("-created_at")

    return render(
        request,
        "exam/reviews.html",
        {
            "reviews": reviews
        }
    )



# For Testing Purpose

# def test500(request):
#     x = 10 / 0
    