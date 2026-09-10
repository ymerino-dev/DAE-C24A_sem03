from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    statement = models.TextField()
    score = models.IntegerField(default=1)

    class Meta:
        ordering = ["id"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.statement[:100]


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return self.text[:100]
