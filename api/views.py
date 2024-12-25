from django.shortcuts import get_list_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.models import (
    Course, 
    User, 
    Presentation, 
    Feedback,
    FeedbackComment,
)
from api.serializers import (
    CourseSerializer, 
    UserSerializer, 
    PresentationSerializer, 
    FeedbackSerializer, 
    FeedbackCommentSerializer,
)


class UserProfile(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # This is an example of how to dynamically set permissions based on the request method
    # def get_permissions(self):
    #     self.permission_classes = [AllowAny]
    #     if self.request.method == 'POST':
    #         self.permission_classes = [IsAdminUser]
    #     return super().get_permissions()


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class PresentationList(generics.ListAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = [IsAuthenticated]


class PresentationDetail(generics.RetrieveAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    lookup_url_kwarg = 'presentation_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class FeedbackList(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        presentation_id = self.kwargs.get('presentation_id')
        return get_list_or_404(Feedback, presentation_id=presentation_id)


class FeedbackCommentList(generics.ListAPIView):
    serializer_class = FeedbackCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        feedback_id = self.kwargs.get('feedback_id')
        return get_list_or_404(FeedbackComment, feedback_id=feedback_id)

