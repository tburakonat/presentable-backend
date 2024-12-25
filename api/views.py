from django.shortcuts import get_list_or_404
from rest_framework.exceptions import NotFound
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
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


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class UserRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    lookup_field = 'id'

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'
    lookup_field = 'id'

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class PresentationListCreate(generics.ListCreateAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class PresentationRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    lookup_url_kwarg = 'presentation_id'
    lookup_field = 'id'

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class FeedbackListCreate(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        presentation_id = self.kwargs.get('presentation_id')
        return get_list_or_404(Feedback, presentation_id=presentation_id)
    
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class FeedbackRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackSerializer
    lookup_url_kwarg = 'feedback_id'
    lookup_field = 'id'

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


    def get_queryset(self):
        presentation_id = self.kwargs.get('presentation_id')
        return Feedback.objects.filter(presentation_id=presentation_id)


    def get_object(self):
        queryset = self.get_queryset()
        feedback_id = self.kwargs.get('feedback_id')
        
        try:
            obj = queryset.get(id=feedback_id)
        except Feedback.DoesNotExist:
            raise NotFound(detail="Feedback not found.")
        
        return obj


class FeedbackCommentListCreate(generics.ListCreateAPIView):
    serializer_class = FeedbackCommentSerializer

    def get_queryset(self):
        feedback_id = self.kwargs.get('feedback_id')
        return get_list_or_404(FeedbackComment, feedback_id=feedback_id)
    
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class FeedbackCommentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackCommentSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


    def get_queryset(self):
        feedback_id = self.kwargs.get('feedback_id')
        return FeedbackComment.objects.filter(feedback_id=feedback_id)

    def get_object(self):
        queryset = self.get_queryset()
        comment_id = self.kwargs.get('comment_id')
        
        try:
            obj = queryset.get(id=comment_id)
        except FeedbackComment.DoesNotExist:
            raise NotFound(detail="Comment not found.")

        return obj

