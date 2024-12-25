from django.urls import path
from api import views

urlpatterns = [
    path('me/', views.UserProfile.as_view()),
    path('users/', views.UserListCreate.as_view()),
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:course_id>/', views.CourseDetail.as_view()),
    path('presentations/', views.PresentationList.as_view()),
    path('presentations/<int:presentation_id>/', views.PresentationDetail.as_view()),
    path('presentations/<int:presentation_id>/feedback/', views.FeedbackList.as_view()),
    path('feedback/<int:feedback_id>/comments/', views.FeedbackCommentList.as_view()),
]
