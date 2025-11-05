"""
APPLICATION MODEL
=================
This file defines the Application model which links Applicants to Jobs.

KEY CONCEPTS:
- ForeignKey: Creates a relationship between models (like a link)
- on_delete=CASCADE: If applicant/job is deleted, delete their applications too
- UniqueConstraint: Prevents duplicate applications (same applicant + job)
"""

from django.db import models
from applicants.models import Applicant
from jobs.models import Job


class Application(models.Model):
    """
    Represents a job application (an applicant applying for a job).
    
    This is a "many-to-many" relationship with extra data:
    - One applicant can apply to many jobs
    - One job can have many applicants
    - The Application model stores when they applied and the status
    """
    
    # Status choices: Defines allowed values for the status field
    STATUS_CHOICES = [
        ('applied', 'Applied'),           # Default status
        ('shortlisted', 'Shortlisted'),   # Applicant was shortlisted
        ('rejected', 'Rejected'),         # Application rejected
    ]
    
    # ForeignKey: Links this application to an Applicant
    # When you access application.applicant, you get the full Applicant object
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,  # Delete applications if applicant is deleted
        related_name='applications',  # Access applicant's applications via: applicant.applications.all()
        help_text="The applicant who is applying"
    )
    
    # ForeignKey: Links this application to a Job
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,  # Delete applications if job is deleted
        related_name='applications',  # Access job's applications via: job.applications.all()
        help_text="The job being applied for"
    )
    
    # CharField with choices: Only allows values defined in STATUS_CHOICES
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied',  # New applications start with 'applied' status
        help_text="Current status of the application"
    )
    
    applied_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When the application was submitted"
    )
    
    class Meta:
        ordering = ['-applied_on']  # Newest applications first
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        
        # IMPORTANT: This prevents duplicate applications
        # Same applicant cannot apply twice for the same job
        constraints = [
            models.UniqueConstraint(
                fields=['applicant', 'job'],
                name='unique_applicant_job'
            )
        ]
    
    def __str__(self):
        """String representation showing who applied for what"""
        return f"{self.applicant.name} -> {self.job.title} ({self.status})"
