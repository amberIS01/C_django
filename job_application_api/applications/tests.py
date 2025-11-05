"""
UNIT TESTS FOR APPLICATION API
===============================

WHAT ARE TESTS?
Tests are automated checks to ensure your code works correctly.

HOW TO RUN TESTS:
    python manage.py test applications

TESTING CONCEPTS:
- setUp(): Runs before each test (creates test data)
- Test methods: Start with 'test_' (e.g., test_create_application)
- Assertions: Check if results match expectations (assertEqual, assertTrue, etc.)
- Test database: Django creates a temporary database for tests
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from applicants.models import Applicant
from jobs.models import Job
from applications.models import Application


class ApplicationModelTest(TestCase):
    """
    Test the Application model directly (without API).
    """
    
    def setUp(self):
        """
        Create test data before each test.
        setUp() is called automatically before each test method.
        """
        # Create test applicant
        self.applicant = Applicant.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890"
        )
        
        # Create test job
        self.job = Job.objects.create(
            title="Python Developer",
            description="Build Django applications"
        )
    
    def test_create_application(self):
        """
        Test creating an application.
        """
        application = Application.objects.create(
            applicant=self.applicant,
            job=self.job
        )
        
        # Check if application was created with correct defaults
        self.assertEqual(application.status, 'applied')
        self.assertEqual(application.applicant, self.applicant)
        self.assertEqual(application.job, self.job)
    
    def test_duplicate_application_prevented(self):
        """
        Test that duplicate applications are prevented by database constraint.
        """
        # Create first application
        Application.objects.create(
            applicant=self.applicant,
            job=self.job
        )
        
        # Try to create duplicate (should fail)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Application.objects.create(
                applicant=self.applicant,
                job=self.job
            )


class ApplicationAPITest(APITestCase):
    """
    Test the Application API endpoints.
    
    APITestCase provides:
    - self.client: For making HTTP requests
    - Authentication handling
    - JSON response parsing
    """
    
    def setUp(self):
        """
        Set up test data and authentication.
        """
        # Create a test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test applicant
        self.applicant = Applicant.objects.create(
            name="Jane Smith",
            email="jane@example.com"
        )
        
        # Create test job
        self.job = Job.objects.create(
            title="Django Developer",
            description="Build REST APIs"
        )
        
        # Authenticate the client
        # This simulates a logged-in user
        self.client.force_authenticate(user=self.user)
    
    def test_apply_for_job_success(self):
        """
        Test successfully applying for a job via /api/apply/
        """
        url = '/api/apply/'
        data = {
            'applicant_id': self.applicant.id,
            'job_id': self.job.id
        }
        
        # Make POST request
        response = self.client.post(url, data, format='json')
        
        # Check response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response contains success message
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Application submitted successfully')
        
        # Check application was created in database
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.first()
        self.assertEqual(application.applicant, self.applicant)
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.status, 'applied')
    
    def test_apply_for_job_duplicate(self):
        """
        Test that duplicate applications are rejected.
        """
        # Create first application
        Application.objects.create(
            applicant=self.applicant,
            job=self.job
        )
        
        # Try to apply again
        url = '/api/apply/'
        data = {
            'applicant_id': self.applicant.id,
            'job_id': self.job.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should get 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Should have error message
        self.assertIn('error', response.data)
        
        # Should still only have 1 application
        self.assertEqual(Application.objects.count(), 1)
    
    def test_apply_for_nonexistent_job(self):
        """
        Test applying for a job that doesn't exist.
        """
        url = '/api/apply/'
        data = {
            'applicant_id': self.applicant.id,
            'job_id': 99999  # Doesn't exist
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should get 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_applications(self):
        """
        Test listing all applications.
        """
        # Create multiple applications
        job2 = Job.objects.create(title="React Developer", description="Build UIs")
        Application.objects.create(applicant=self.applicant, job=self.job)
        Application.objects.create(applicant=self.applicant, job=job2)
        
        url = '/api/applications/'
        response = self.client.get(url)
        
        # Should get 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should have 2 applications
        # Note: With pagination, results are in 'results' key
        self.assertEqual(len(response.data['results']), 2)
    
    def test_update_application_status(self):
        """
        Test updating application status via PATCH.
        """
        # Create application
        application = Application.objects.create(
            applicant=self.applicant,
            job=self.job
        )
        
        url = f'/api/applications/{application.id}/'
        data = {'status': 'shortlisted'}
        
        response = self.client.patch(url, data, format='json')
        
        # Should get 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check status was updated
        application.refresh_from_db()  # Reload from database
        self.assertEqual(application.status, 'shortlisted')
    
    def test_authentication_required(self):
        """
        Test that authentication is required for API access.
        """
        # Create unauthenticated client
        client = APIClient()
        
        url = '/api/applications/'
        response = client.get(url)
        
        # Should get 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ==============================================================================
# HOW TO RUN THESE TESTS
# ==============================================================================
"""
1. Run all tests:
   python manage.py test

2. Run tests for specific app:
   python manage.py test applications

3. Run specific test class:
   python manage.py test applications.tests.ApplicationAPITest

4. Run specific test method:
   python manage.py test applications.tests.ApplicationAPITest.test_apply_for_job_success

5. Run with verbose output:
   python manage.py test --verbosity=2

WHAT TO EXPECT:
- Tests create a temporary database
- Each test is independent (setUp creates fresh data)
- Tests clean up after themselves
- You'll see: Ran X tests in Y seconds, OK (or FAILED)
"""
