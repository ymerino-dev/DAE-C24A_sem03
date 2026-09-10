from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "quiz/exam_list.html", {"exams": exams})


def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all()
    return render(
        request,
        "quiz/exam_detail.html",
        {"exam": exam, "questions": questions},
    )


def question_add(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST, instance=exam)
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
                    return redirect("exam_detail", pk=exam.pk)
            else:
                question.delete()
        messages.error(request, "Please correct the errors below.")
    else:
        form = QuestionForm()
        formset = ChoiceFormSet(instance=exam)
    return render(
        request,
        "quiz/question_add.html",
        {"form": form, "formset": formset, "exam": exam},
    )
