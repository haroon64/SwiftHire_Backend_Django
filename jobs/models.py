from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from recruiter.models import Recruiter

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
        ("remote", "Remote"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
   
    salary_min = models.IntegerField(max_length=10, null=True, blank=True)
    salary_max =  models.IntegerField(max_length=10, null=True, blank=True)
    fixed_salary = models.IntegerField(max_length=10, null=True, blank=True)

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name="jobs")
   
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Python-level validation (runs in Admin and Forms)"""
        # Logic: Either fixed_salary exists, OR both min and max exist.
        has_fixed = self.fixed_salary is not None
        has_range = self.salary_min is not None and self.salary_max is not None

        if not (has_fixed ^ has_range): # Using XOR for "exclusive or"
            raise ValidationError(
                "You must provide either a Fixed Salary OR both Salary Min and Max."
            )
        
        if has_range and self.salary_min > self.salary_max:
            raise ValidationError("Minimum salary cannot be greater than maximum salary.")

    def save(self, *args, **kwargs):
        self.full_clean() # Ensures clean() is called before saving to DB
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            # Database-level validation
            models.CheckConstraint(
                condition=(
                    models.Q(fixed_salary__isnull=False, salary_min__isnull=True, salary_max__isnull=True) |
                    models.Q(fixed_salary__isnull=True, salary_min__isnull=False, salary_max__isnull=False)
                ),
                name="enforce_salary_format"
            )
        ]

    def __str__(self):
        return self.title