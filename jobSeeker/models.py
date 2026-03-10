from django.db import models
from django.conf import settings


class JobSeekerProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("others", "Others"),

    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobseeker_profile"
    )


    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)

    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)

    profile_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["current_location"]),
      
        ]

    def __str__(self):
        return f"{self.user.email} - JobSeeker"