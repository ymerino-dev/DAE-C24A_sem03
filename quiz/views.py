from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet


class ExamListView(View):
    def get(self, request):
        exams = Exam.objects.all()
        return render(request, "quiz/exam_list.html", {"exams": exams})


class ExamDetailView(View):
    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        questions = exam.questions.all()
        return render(
            request,
            "quiz/exam_detail.html",
            {"exam": exam, "questions": questions},
        )


class ExamCreateView(View):
    form_class = ExamForm
    template_name = "quiz/exam_form.html"
    success_url = reverse_lazy("quiz:exam_list")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam created successfully.")
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})


def question_add(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                correct_count = 0
                for cleaned_form in formset.cleaned_forms:
                    if cleaned_form and cleaned_form.cleaned_data.get("is_correct"):
                        correct_count += 1
                if correct_count != 1:
                    messages.error(
                        request,
                        "Exactly one option must be marked as correct.",
                    )
                    formset.delete()
                    question.delete()
                else:
                    formset.save()
                    messages.success(
                        request,
                        "Question added successfully.",
                    )
                    return redirect("quiz:exam_detail", pk=exam.pk)
            else:
                question.delete()
        messages.error(request, "Please correct the errors below.")
    else:
        form = QuestionForm()
        formset = ChoiceFormSet(instance=Question(exam=exam))
    return render(
        request,
        "quiz/question_add.html",
        {"form": form, "formset": formset, "exam": exam},
    )
