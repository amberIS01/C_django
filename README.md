# Django REST API Projects

This repository contains two Django REST Framework projects demonstrating different API architectures and features.

## 📦 Projects Overview

### Project 1: Job Application Management API
A complete job application management system with CRUD operations, authentication, and search capabilities.

**Features:**
- ✅ Applicant management (CRUD)
- ✅ Job posting management (CRUD)
- ✅ Job application system with duplicate prevention
- ✅ Application status tracking (applied/shortlisted/rejected)
- ✅ Search and filter applicants by name/email
- ✅ JWT authentication
- ✅ Pagination (10 items per page)
- ✅ Unit tests
- ✅ File upload support (resumes)

### Project 2: Sales Analytics API
A sales analytics system with complex data relationships, nested serializers, and advanced query optimization.

**Features:**
- ✅ Customer, Product, and Order management (CRUD)
- ✅ Nested order creation (orders with multiple items)
- ✅ Analytics endpoints (sales summary, top customers, top products)
- ✅ Query optimization (select_related, prefetch_related, annotate)
- ✅ Date range filtering for analytics
- ✅ JWT authentication
- ✅ Pagination
- ✅ Unit tests for analytics

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amberIS01/C_django.git
   cd C_django
   ```

2. **Set up environment variables (optional):**
   ```bash
   copy .env.example .env
   # Edit .env with your settings if needed
   ```

---

## 📋 Project 1: Job Application Management API

### Setup

1. **Navigate to project directory:**
   ```bash
   cd job_application_api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations (create database tables):**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create username and password
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Server will start at: http://localhost:8000

### API Endpoints

#### Authentication
- `POST /api/token/` - Get JWT tokens (login)
  ```bash
  curl -X POST http://localhost:8000/api/token/ \
    -H "Content-Type: application/json" \
    -d '{"username": "your_username", "password": "your_password"}'
  ```

- `POST /api/token/refresh/` - Refresh access token
  ```bash
  curl -X POST http://localhost:8000/api/token/refresh/ \
    -H "Content-Type: application/json" \
    -d '{"refresh": "your_refresh_token"}'
  ```

#### Applicants
- `GET /api/applicants/` - List all applicants (with pagination and search)
- `POST /api/applicants/` - Create new applicant
- `GET /api/applicants/{id}/` - Get specific applicant
- `PUT /api/applicants/{id}/` - Update applicant
- `DELETE /api/applicants/{id}/` - Delete applicant

**Search Example:**
```bash
curl -X GET "http://localhost:8000/api/applicants/?search=john" \
  -H "Authorization: Bearer your_access_token"
```

#### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create new job
- `GET /api/jobs/{id}/` - Get specific job
- `PUT /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job

#### Applications
- `GET /api/applications/` - List all applications
- `POST /api/apply/` - Apply for a job
  ```json
  {
    "applicant_id": 1,
    "job_id": 2
  }
  ```
- `PATCH /api/applications/{id}/` - Update application status
  ```json
  {
    "status": "shortlisted"
  }
  ```

### Testing

Run tests:
```bash
python manage.py test
```

Run specific test:
```bash
python manage.py test applications.tests.ApplicationAPITest
```

---

## 📊 Project 2: Sales Analytics API

### Setup

1. **Navigate to project directory:**
   ```bash
   cd sales_analytics_api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver 8001
   ```
   Server will start at: http://localhost:8001 (different port to avoid conflict)

### API Endpoints

#### Authentication
Same as Project 1 (`/api/token/`, `/api/token/refresh/`)

#### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get specific customer
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

#### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get specific product
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

#### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create new order with items
  ```json
  {
    "customer": 1,
    "items": [
      {"product": 1, "quantity": 2},
      {"product": 2, "quantity": 1}
    ]
  }
  ```
- `GET /api/orders/{id}/` - Get specific order
- `PUT /api/orders/{id}/` - Update order

**Filter Examples:**
```bash
# Filter by customer
curl "http://localhost:8001/api/orders/?customer=1" \
  -H "Authorization: Bearer your_access_token"

# Filter by date range
curl "http://localhost:8001/api/orders/?from=2024-01-01&to=2024-12-31" \
  -H "Authorization: Bearer your_access_token"
```

#### Analytics
- `GET /api/analytics/sales-summary/` - Overall sales statistics
  - Returns: total sales, total orders, total customers, total products sold
  
- `GET /api/analytics/top-customers/` - Top 5 customers by spending
  
- `GET /api/analytics/top-products/` - Top 5 most sold products

**Analytics with Date Range:**
```bash
curl "http://localhost:8001/api/analytics/sales-summary/?from=2024-01-01&to=2024-12-31" \
  -H "Authorization: Bearer your_access_token"
```

### Testing

Run tests:
```bash
python manage.py test
```

Run analytics tests only:
```bash
python manage.py test analytics
```

---

## 🔐 Authentication Guide

Both projects use JWT (JSON Web Token) authentication.

### Step-by-Step Authentication:

1. **Create a user (via Django admin):**
   - Go to http://localhost:8000/admin/
   - Login with superuser credentials
   - Create a new user

2. **Get access token:**
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```
   
   Response:
   ```json
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
   }
   ```

3. **Use access token in requests:**
   ```bash
   curl -X GET http://localhost:8000/api/applicants/ \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
   ```

4. **Refresh token when expired:**
   ```bash
   curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "your_refresh_token"}'
   ```

**Token Lifetimes:**
- Access token: 1 hour
- Refresh token: 7 days

---

## 📚 Understanding the Code

### Project Structure

```
job_application_api/
├── applicants/           # Applicant app
│   ├── models.py        # Database model for Applicant
│   ├── serializers.py   # JSON conversion for Applicant
│   ├── views.py         # API endpoints for Applicant
│   └── urls.py          # URL routing for Applicant
├── jobs/                # Job app (similar structure)
├── applications/        # Application app (similar structure)
└── job_application_api/ # Main project settings
    ├── settings.py      # Project configuration
    └── urls.py          # Main URL routing
```

### Key Django Concepts

#### 1. Models (models.py)
Models define your database tables. Each model class becomes a table.

Example:
```python
class Applicant(models.Model):
    name = models.CharField(max_length=100)  # VARCHAR column
    email = models.EmailField(unique=True)   # Email with validation
```

#### 2. Serializers (serializers.py)
Serializers convert between Python objects and JSON.

```python
# Incoming JSON → Python object → Save to database
# Database object → Python object → Outgoing JSON
```

#### 3. Views (views.py)
Views handle HTTP requests and return responses.

```python
# GET request → Query database → Return JSON
# POST request → Validate data → Create object → Return JSON
```

#### 4. URLs (urls.py)
URLs map web addresses to views.

```python
# /api/applicants/ → ApplicantViewSet → list() method
# /api/applicants/5/ → ApplicantViewSet → retrieve() method
```

---

## 🛠️ Common Tasks

### Adding a New Field to a Model

1. Edit the model:
   ```python
   # In models.py
   class Applicant(models.Model):
       # ... existing fields ...
       linkedin = models.URLField(blank=True, null=True)  # New field
   ```

2. Create and run migration:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Creating Test Data

Use Django admin or shell:
```bash
python manage.py shell
```

```python
from applicants.models import Applicant
Applicant.objects.create(
    name="John Doe",
    email="john@example.com",
    phone="1234567890"
)
```

### Viewing All API Endpoints

Visit http://localhost:8000/api/ in your browser (when server is running).
Django REST Framework provides a browsable API interface.

---

## 🐛 Troubleshooting

### Issue: "No such table" error
**Solution:** Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Unauthorized" (401) error
**Solution:** Make sure you're including the JWT token:
```bash
-H "Authorization: Bearer your_access_token"
```

### Issue: "Token has expired"
**Solution:** Use refresh token to get a new access token:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

### Issue: Port already in use
**Solution:** Use a different port:
```bash
python manage.py runserver 8001
```

---

## 📖 API Testing Tools

### 1. cURL (Command Line)
```bash
curl -X GET http://localhost:8000/api/applicants/ \
  -H "Authorization: Bearer token_here"
```

### 2. Postman
1. Download from https://www.postman.com/
2. Import collection:
   - Method: GET, POST, PUT, DELETE
   - URL: http://localhost:8000/api/applicants/
   - Headers: Authorization: Bearer {token}

### 3. Django Browsable API
Just visit http://localhost:8000/api/ in your browser!

---

## 🧪 Running Tests

### Project 1 Tests
```bash
cd job_application_api
python manage.py test applications
```

### Project 2 Tests
```bash
cd sales_analytics_api
python manage.py test analytics
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📝 Assignment Requirements Checklist

### Project 1: Job Application Management API
- ✅ Models: Applicant, Job, Application with proper relationships
- ✅ CRUD operations for all models
- ✅ Duplicate application prevention
- ✅ Search filter on applicants
- ✅ Status update endpoint
- ✅ JWT authentication (Bonus)
- ✅ Pagination (Bonus)
- ✅ Unit tests (Bonus)

### Project 2: Sales Analytics API
- ✅ Models: Customer, Product, Order, OrderItem
- ✅ Nested serializers for orders
- ✅ Query optimization (select_related, annotate)
- ✅ Analytics endpoints (sales summary, top customers, top products)
- ✅ Date range filters (Bonus)
- ✅ JWT authentication (Bonus)
- ✅ Pagination (Bonus)
- ✅ Unit tests (Bonus)

---

## 🤝 Contributing

This is a test assignment repository. For learning purposes only.

---

## 📄 License

This project is created for educational and assessment purposes.

---

## 👨‍💻 Author

Created as part of Django Developer Test Assignment

---

## 📞 Support

For questions about the code, please refer to:
- Inline code comments (every file has detailed explanations)
- This README
- Django documentation: https://docs.djangoproject.com/
- DRF documentation: https://www.django-rest-framework.org/

---

## 🎯 Interview Preparation Notes

### Key Points to Explain:

1. **Models & Relationships:**
   - ForeignKey creates many-to-one relationships
   - UniqueConstraint prevents duplicates
   - Properties (like `total_price`) for calculated fields

2. **Serializers:**
   - ModelSerializer automatically creates fields
   - Nested serializers for complex data
   - Custom validation methods

3. **Views:**
   - ViewSets provide CRUD operations automatically
   - Query optimization reduces database queries
   - Filters and pagination for better UX

4. **Authentication:**
   - JWT tokens are stateless and scalable
   - Access token for requests, refresh token for renewal
   - Bearer token in Authorization header

5. **Testing:**
   - APITestCase for testing endpoints
   - Separate test database (doesn't affect real data)
   - Tests ensure code works as expected

### Be Ready to Discuss:
- Why you chose certain design patterns
- How you handled validation
- Query optimization techniques used
- How to extend the API with new features
- Security considerations (authentication, validation, etc.)

**Good luck with your interview! 🚀**

