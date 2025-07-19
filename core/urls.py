from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, QuestionViewSet, TestCaseViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('courses', CourseViewSet, basename='course')
router.register('testcases', TestCaseViewSet)
#router.register('submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
