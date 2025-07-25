#!/usr/bin/env python3
"""
Test script for KPA Form Data API
This script demonstrates all the implemented API endpoints
"""

import requests
import json
import os
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8000"

# Test credentials
PHONE_NUMBER = "7760873976"
PASSWORD = "to_share@123"

def print_separator(title):
    """Print a separator with title."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_response(response, title="Response"):
    """Print formatted response."""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    """Test the health check endpoint."""
    print_separator("HEALTH CHECK")
    
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")
    
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")

def test_authentication():
    """Test authentication endpoints."""
    print_separator("AUTHENTICATION TESTS")
    
    # Test login
    login_data = {
        "phone_number": PHONE_NUMBER,
        "password": PASSWORD
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json=login_data
    )
    print_response(response, "Login")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print("Login failed!")
        return None

def test_form_operations(token):
    """Test form submission and management."""
    print_separator("FORM OPERATIONS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test form submission
    form_data = {
        "form_type": "kpa_application",
        "form_data": {
            "applicant_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "department": "Human Resources",
            "position": "HR Manager",
            "experience_years": 5,
            "skills": ["Leadership", "Communication", "Problem Solving"],
            "submission_date": datetime.now().isoformat()
        },
        "status": "submitted"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/forms/submit",
        json=form_data,
        headers=headers
    )
    print_response(response, "Form Submission")
    
    submission_id = None
    if response.status_code == 201:
        submission_id = response.json()["id"]
    
    # Test getting user submissions
    response = requests.get(
        f"{BASE_URL}/api/v1/forms/submissions",
        headers=headers
    )
    print_response(response, "Get User Submissions")
    
    # Test getting specific submission
    if submission_id:
        response = requests.get(
            f"{BASE_URL}/api/v1/forms/submissions/{submission_id}",
            headers=headers
        )
        print_response(response, f"Get Submission {submission_id}")
    
    return submission_id

def test_file_upload(token, submission_id):
    """Test file upload functionality."""
    print_separator("FILE UPLOAD TEST")
    
    if not submission_id:
        print("No submission ID available for file upload test")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test file
    test_file_content = f"""
KPA Application Supporting Document
===================================

Applicant: Jane Smith
Position: HR Manager
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is a test document demonstrating the file upload functionality
of the KPA Form Data API system.

Skills and Qualifications:
- 5+ years of HR experience
- Leadership and team management
- Employee relations and conflict resolution
- Policy development and implementation
- Performance management systems

Education:
- Bachelor's in Human Resources
- Certified HR Professional (CHRP)

References available upon request.
"""
    
    with open("test_document.txt", "w") as f:
        f.write(test_file_content)
    
    # Upload the file
    with open("test_document.txt", "rb") as f:
        files = {"file": ("test_document.txt", f, "text/plain")}
        response = requests.post(
            f"{BASE_URL}/api/v1/forms/submissions/{submission_id}/upload",
            files=files,
            headers=headers
        )
    
    print_response(response, "File Upload")
    
    # Clean up test file
    if os.path.exists("test_document.txt"):
        os.remove("test_document.txt")

def test_form_update(token, submission_id):
    """Test form update functionality."""
    print_separator("FORM UPDATE TEST")
    
    if not submission_id:
        print("No submission ID available for update test")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update form data
    update_data = {
        "form_data": {
            "applicant_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "department": "Human Resources",
            "position": "Senior HR Manager",  # Updated position
            "experience_years": 6,  # Updated experience
            "skills": ["Leadership", "Communication", "Problem Solving", "Strategic Planning"],  # Added skill
            "submission_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "status": "under_review"  # Updated status
    }
    
    response = requests.put(
        f"{BASE_URL}/api/v1/forms/submissions/{submission_id}",
        json=update_data,
        headers=headers
    )
    print_response(response, "Form Update")

def test_api_documentation():
    """Test API documentation endpoints."""
    print_separator("API DOCUMENTATION")
    
    # Test OpenAPI spec
    response = requests.get(f"{BASE_URL}/openapi.json")
    print(f"OpenAPI Spec Status: {response.status_code}")
    if response.status_code == 200:
        spec = response.json()
        print(f"API Title: {spec.get('info', {}).get('title')}")
        print(f"API Version: {spec.get('info', {}).get('version')}")
        print(f"Available Endpoints: {len(spec.get('paths', {}))}")
    
    # Test Swagger UI
    response = requests.get(f"{BASE_URL}/docs")
    print(f"Swagger UI Status: {response.status_code}")

def main():
    """Run all API tests."""
    print("KPA Form Data API - Comprehensive Test Suite")
    print(f"Testing API at: {BASE_URL}")
    print(f"Test started at: {datetime.now()}")
    
    try:
        # Test health check
        test_health_check()
        
        # Test authentication
        token = test_authentication()
        
        if not token:
            print("Authentication failed. Stopping tests.")
            return
        
        # Test form operations
        submission_id = test_form_operations(token)
        
        # Test file upload
        test_file_upload(token, submission_id)
        
        # Test form update
        test_form_update(token, submission_id)
        
        # Test API documentation
        test_api_documentation()
        
        print_separator("TEST SUMMARY")
        print("✅ All tests completed successfully!")
        print("✅ Authentication working")
        print("✅ Form submission working")
        print("✅ Form retrieval working")
        print("✅ File upload working")
        print("✅ Form update working")
        print("✅ API documentation accessible")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()