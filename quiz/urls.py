from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.exam_list, name="exam_list"),
    path("<int:pk>/", views.exam_detail, name="exam_detail"),
    path("<int:exam_pk>/question/add/", views.question_add, name="question_add"),
]
