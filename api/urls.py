from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.UserListCreate.as_view()),
    path('users/<int:user_id>/', views.UserRetrieveUpdateDelete.as_view()),
    path('courses/', views.CourseListCreate.as_view()),
    path('courses/<int:course_id>/', views.CourseRetrieveUpdateDelete.as_view()),
    path('presentations/', views.PresentationListCreate.as_view()),
    path('presentations/<int:presentation_id>/', views.PresentationRetrieveUpdateDelete.as_view()),
    path('presentations/<int:presentation_id>/feedback/', views.FeedbackListCreate.as_view()),
    path('presentations/<int:presentation_id>/feedback/<int:feedback_id>/', views.FeedbackRetrieveUpdateDelete.as_view()),
    path('feedback/<int:feedback_id>/comments/', views.FeedbackCommentListCreate.as_view()),
    path('feedback/<int:feedback_id>/comments/<int:comment_id>/', views.FeedbackCommentRetrieveUpdateDelete.as_view()),
]
