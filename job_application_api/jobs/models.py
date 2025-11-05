"""
JOB MODEL
=========
This file defines the Job model which stores information about job openings.

A Job represents a position that applicants can apply for.
"""

from django.db import models


class Job(models.Model):
    """
    Stores information about job openings/positions.
    
    Fields explained:
    - id: Auto-created by Django
    - title: Job position title (e.g., "Django Developer")
    - description: Detailed job description
    - posted_on: When the job was posted (auto-set)
    """
    
    title = models.CharField(
        max_length=100,
        help_text="Job position title"
    )
    
    # TextField: For longer text content (no max length limit)
    description = models.TextField(
        help_text="Detailed job description and requirements"
    )
    
    posted_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When the job was posted"
    )
    
    class Meta:
        ordering = ['-posted_on']  # Newest jobs first
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        """String representation showing job title"""
        return self.title
