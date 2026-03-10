from django.db import models
from django.conf import settings
from jobs.models import Job
from jobSeeker.models import JobSeekerProfile


class Application(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("reviewed", "Reviewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant} - {self.job}"