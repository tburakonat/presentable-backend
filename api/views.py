from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import (
    Course, 
    User, 
    Presentation, 
    Feedback
)
from api.serializers import (
    CourseSerializer, 
    UserSerializer, 
    PresentationSerializer, 
    FeedbackSerializer, 
    FeedbackCommentSerializer,
)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_course_by_id(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_presentations(request):
    presentations = Presentation.objects.all()
    serializer = PresentationSerializer(presentations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_presentation_by_id(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    serializer = PresentationSerializer(presentation)
    return Response(serializer.data)


@api_view(['GET'])
def get_feedback_by_presentation_id(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    feedbacks = presentation.received_feedbacks.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_comments_by_feedback_id(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    comments = feedback.feedback_comments.all()
    serializer = FeedbackCommentSerializer(comments, many=True)
    return Response(serializer.data)