# KPA Form Data API

A FastAPI-based backend system for managing KPA form data with user authentication, form submissions, and file uploads. This project implements RESTful APIs with PostgreSQL database integration.

## Features

### Core Functionality
- **User Authentication**: JWT-based authentication with phone number login
- **Form Management**: Submit, retrieve, update, and delete form submissions
- **File Upload**: Secure file attachment system with validation
- **Database Integration**: PostgreSQL database with SQLAlchemy ORM
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

### Key Features
- **Security**: JWT tokens, password hashing, input validation
- **File Handling**: Support for multiple file types with size limits
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Docker Support**: Containerized deployment with Docker Compose

## Technology Stack

- **Backend**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.23
- **Authentication**: JWT with python-jose, bcrypt password hashing
- **File Upload**: python-multipart for form data handling
- **Containerization**: Docker & Docker Compose
- **Python**: 3.11+

## Installation & Setup

### Method 1: Using Docker (Recommended)

1. **Clone the Repository**
```bash
git clone <repository-url>
cd kpa-form-api
```

2. **Run with Docker Compose**
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Method 2: Local Development

1. **Clone the Repository**
```bash
git clone <repository-url>
cd kpa-form-api
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL Database**
```bash
# Create database
createdb kpa_forms

# Or using psql
psql -c "CREATE DATABASE kpa_forms;"
```

5. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Initialize Database**
```bash
python init_db.py
```

7. **Run Development Server**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Default Login Credentials

For testing purposes, a default user is created:
- **Phone Number**: `7760873976`
- **Password**: `to_share@123`

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login user and get JWT token |
| GET | `/api/v1/auth/me` | Get current user information |
| POST | `/api/v1/auth/logout` | Logout user |

### Form Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/forms/submit` | Submit a new form |
| GET | `/api/v1/forms/submissions` | Get user's form submissions |
| GET | `/api/v1/forms/submissions/{id}` | Get specific form submission |
| PUT | `/api/v1/forms/submissions/{id}` | Update form submission |
| DELETE | `/api/v1/forms/submissions/{id}` | Delete form submission |
| POST | `/api/v1/forms/submissions/{id}/upload` | Upload file attachment |
| GET | `/api/v1/forms/types` | Get available form types |

## Project Structure

```
kpa-form-api/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration
├── models.py               # SQLAlchemy database models
├── schemas.py              # Pydantic request/response schemas
├── auth_utils.py           # Authentication utilities
├── init_db.py              # Database initialization script
├── routers/                # API route modules
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   └── forms.py            # Form management routes
├── uploads/                # File upload directory
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env                    # Environment variables
└── README.md               # Project documentation
```

## Database Models

### User
- Phone number (unique identifier)
- Password hash
- Full name and email
- Account status and timestamps
- Relationship with form submissions

### FormSubmission
- User association
- Form type and JSON data
- Submission status and timestamps
- Relationship with file attachments

### FileAttachment
- Form submission association
- File metadata (name, type, size, path)
- Upload timestamp

## Usage Examples

### 1. User Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "1234567890",
    "password": "securepassword",
    "full_name": "John Doe",
    "email": "john@example.com"
  }'
```

### 2. User Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "7760873976",
    "password": "to_share@123"
  }'
```

### 3. Submit Form
```bash
curl -X POST "http://localhost:8000/api/v1/forms/submit" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "form_type": "application_form",
    "form_data": {
      "name": "John Doe",
      "age": 30,
      "purpose": "Job Application"
    }
  }'
```

### 4. Upload File
```bash
curl -X POST "http://localhost:8000/api/v1/forms/submissions/1/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@document.pdf"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/kpa_forms` |
| `SECRET_KEY` | JWT secret key | `your-super-secret-key-here-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | `30` |
| `PORT` | Application port | `8000` |

### File Upload Limits

- **Allowed file types**: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG, GIF
- **Maximum file size**: 10MB
- **Upload directory**: `uploads/`

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Input Validation**: Pydantic schemas for request validation
- **File Type Validation**: Restricted file extensions and size limits
- **CORS Configuration**: Configurable cross-origin resource sharing

## Testing

The API can be tested using:

1. **Swagger UI**: Interactive testing at `/docs`
2. **Postman**: Import the generated OpenAPI specification
3. **curl**: Command-line testing (examples above)
4. **Python requests**: Programmatic testing

## Deployment

### Production Deployment

1. **Update Environment Variables**
```bash
# Use strong secret key
SECRET_KEY=your-production-secret-key

# Use production database
DATABASE_URL=postgresql://user:password@host:port/database
```

2. **Deploy with Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Set up Reverse Proxy** (Nginx example)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Limitations & Assumptions

- Phone number is used as the primary identifier for users
- File uploads are stored locally (consider cloud storage for production)
- JWT tokens don't have refresh mechanism (implement for production)
- Form data is stored as JSON (flexible but less structured)
- No email verification implemented
- Basic file type validation (can be enhanced)

## Future Enhancements

- Email verification system
- Refresh token mechanism
- Cloud storage integration (AWS S3, Google Cloud)
- Advanced form validation
- Audit logging
- Rate limiting
- API versioning
- Comprehensive test suite
- CI/CD pipeline
- Monitoring and logging integration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the API documentation at `/docs`
2. Review the code comments
3. Create an issue in the repository
4. Contact: `contact@suvidhaen.com`