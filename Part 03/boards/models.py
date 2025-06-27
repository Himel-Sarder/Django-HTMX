from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)  # To sort lists

    def __str__(self):
        return f"{self.name} ({self.board.name})"


class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
