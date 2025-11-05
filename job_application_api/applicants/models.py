"""
APPLICANT MODEL
===============
This file defines the Applicant model which stores information about job applicants.

KEY CONCEPTS:
- Model: A Python class that represents a database table
- Each field becomes a column in the database
- Django automatically creates an 'id' field as primary key
"""

from django.db import models


class Applicant(models.Model):
    """
    Stores information about job applicants.
    
    Fields explained:
    - id: Auto-created by Django, unique identifier for each applicant
    - name: Applicant's full name (max 100 characters)
    - email: Unique email address (no two applicants can have same email)
    - phone: Optional phone number (max 15 characters)
    - resume: Optional file upload (stored in 'resumes/' folder)
    - applied_on: Automatically set to current date/time when applicant is created
    """
    
    # CharField: For storing text with a maximum length
    name = models.CharField(
        max_length=100,
        help_text="Applicant's full name"
    )
    
    # EmailField: Special field that validates email format
    # unique=True: No two applicants can have the same email
    email = models.EmailField(
        unique=True,
        help_text="Unique email address"
    )
    
    # blank=True, null=True: Makes this field optional
    phone = models.CharField(
        max_length=15,
        blank=True,  # Optional in forms/API
        null=True,   # Optional in database
        help_text="Contact phone number (optional)"
    )
    
    # FileField: For uploading files (resumes in this case)
    # upload_to: Specifies the folder where files will be stored
    resume = models.FileField(
        upload_to='resumes/',  # Files go to media/resumes/
        blank=True,
        null=True,
        help_text="Resume file (optional)"
    )
    
    # DateTimeField: Stores date and time
    # auto_now_add=True: Automatically set to current time when created
    applied_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When the applicant registered"
    )
    
    class Meta:
        """
        Meta options for the model
        - ordering: Default sort order when querying
        - verbose_name: Human-readable name for the model
        """
        ordering = ['-applied_on']  # Newest first (- means descending)
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
    
    def __str__(self):
        """
        String representation of the model
        This is what you see when you print an Applicant object
        """
        return f"{self.name} ({self.email})"
