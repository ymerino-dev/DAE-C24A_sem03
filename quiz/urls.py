from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.ExamListView.as_view(), name="exam_list"),
    path("<int:pk>/", views.ExamDetailView.as_view(), name="exam_detail"),
    path("create/", views.ExamCreateView.as_view(), name="exam_create"),
    path("<int:exam_pk>/question/add/", views.question_add, name="question_add"),
]
