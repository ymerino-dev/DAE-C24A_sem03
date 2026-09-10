from django import forms
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["title", "description"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["statement"]


ChoiceFormSet = forms.inlineformset_factory(
    parent_model=Question,
    model=Choice,
    form=forms.ModelForm,
    fields=["text", "is_correct"],
    extra=2,
    can_delete=True,
)
