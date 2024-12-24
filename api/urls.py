from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.get_all_users),
    path('courses/', views.get_all_courses),
    path('courses/<int:course_id>/', views.get_course_by_id),
    path('presentations/', views.get_all_presentations),
    path('presentations/<int:presentation_id>', views.get_presentation_by_id),
    path('presentations/<int:presentation_id>/feedback', views.get_feedback_by_presentation_id),
    path('feedback/<int:feedback_id>/comments', views.get_comments_by_feedback_id),
]
