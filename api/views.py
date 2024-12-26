from rest_framework.exceptions import NotFound
from api.filters import (
    UserFilter, 
    CourseFilter,
    PresentationFilter,
    FeedbackFilter,
    FeedbackCommentFilter,
)
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
    filterset_class = UserFilter

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
    filterset_class = CourseFilter

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
    filterset_class = PresentationFilter

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
    filterset_class = FeedbackFilter

    def get_queryset(self):
        presentation_id = self.kwargs.get('presentation_id')
        queryset = Feedback.objects.filter(presentation_id=presentation_id)
        if not queryset.exists():
            raise NotFound("No Feedback matches the given query.")
        return queryset

    
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
    filterset_class = FeedbackCommentFilter

    def get_queryset(self):
        feedback_id = self.kwargs.get('feedback_id')
        queryset = FeedbackComment.objects.filter(feedback_id=feedback_id)
        if not queryset.exists():
            raise NotFound("No FeedbackComment matches the given query.")
        return queryset
    
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

