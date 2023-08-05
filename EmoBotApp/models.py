from django.db import models

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Post ID: {self.post_id}, Text: {self.text}"


class LogEntry(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - Command: {self.command}, Message: {self.message}"


# Database model to store user interactions
class UserInteraction(models.Model):
    text = models.TextField()  # Stores the text part of the interaction

    def __str__(self):
        return f"Command: {self.command}, Text: {self.text}"