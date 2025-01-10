from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', views.UserViewSet)
router.register('courses', views.CourseViewSet)
router.register('presentations', views.PresentationViewSet)
router.register('feedbacks', views.FeedbackViewSet)
router.register('comments', views.FeedbackCommentViewSet)

urlpatterns = router.urls
