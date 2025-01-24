from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   class Role(models.TextChoices):
        TEACHER = 'TEACHER'
        STUDENT = 'STUDENT'
        ADMIN = 'ADMIN'
    
   role = models.CharField(max_length=50, choices=Role.choices)


class Course(models.Model):
    """
    Course model with relationships to teachers and students.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    teachers = models.ManyToManyField(
        User, 
        related_name='courses_taught', 
        blank=True
    )
    students = models.ManyToManyField(
        User, 
        related_name='enrolled_courses',  
        blank=True
    )

    def __str__(self):
        return self.name


class Presentation(models.Model):
    """
    Presentation model with a relationship to a course.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    presentation_events = models.JSONField(blank=True, null=True)
    transcription = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presentations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='presentations')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Feedback(models.Model):
    """
    Feedback model with a relationship to a presentation.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_feedbacks')
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='received_feedbacks')

    def __str__(self):
        return f"Feedback {self.id} by {self.created_by.get_full_name()} to the Presentation: {self.presentation}"
    

class FeedbackComment(models.Model):
    """
    FeedbackComments model with a relationship to a feedback.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_feedback_comments')
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='feedback_comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"Comment {self.id} by {self.created_by.get_full_name()} to {self.feedback}"
    
