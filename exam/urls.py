# exam/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('quiz/review/<int:result_id>/', views.quiz_review_view, name='quiz_review'),
    path('quiz/<str:category_name>/<str:difficulty>/', views.take_quiz, name='take_quiz'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path("feedback/", views.feedback_view, name="feedback"),
    path("reviews/", views.reviews_view, name="reviews"),
    
    # path("test500/", views.test500),
    

    # Login aur Logout standard views
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='exam/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    
    # Registration Route (Iska view hum abhi niche banayenge)
    # path('quiz/<str:category_name>/<str:difficulty>/', views.take_quiz, name='take_quiz'),  
]