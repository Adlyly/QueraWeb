from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, QuestionViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
