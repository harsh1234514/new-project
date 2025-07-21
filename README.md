# Django CRM System

A comprehensive Customer Relationship Management (CRM) system built with Django and modern HTML/CSS frontend using Bootstrap 5.

## Features

### Core Functionality
- **Dashboard**: Overview with statistics, recent activities, and quick actions
- **Companies**: Manage company information and track relationships
- **Contacts**: Store and manage contact details with company associations
- **Leads**: Track potential customers through the sales pipeline
- **Deals**: Manage sales opportunities with stages and probability tracking
- **Activities**: Schedule and track tasks, calls, meetings, and notes

### Key Features
- **Modern UI**: Bootstrap 5 with custom styling and responsive design
- **User Authentication**: Django's built-in authentication system
- **Search & Filtering**: Advanced search capabilities across all modules
- **Pagination**: Efficient data handling with paginated views
- **Admin Interface**: Full Django admin integration for data management
- **Database**: SQLite database with proper relationships and constraints

## Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3, Font Awesome 6.0.0
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Python**: 3.13+

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd crm-system
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Default Login Credentials

For quick testing, a default admin user is created:
- **Username**: admin
- **Password**: admin123

## Project Structure

```
crm-system/
├── crm/                    # Main CRM application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   └── urls.py            # URL patterns
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── crm/               # CRM-specific templates
├── static/                # Static files
│   └── css/
│       └── custom.css     # Custom styling
├── crm_project/           # Django project settings
└── requirements.txt       # Python dependencies
```

## Database Models

### Company
- Company information (name, industry, website, contact details)
- Address and location data
- Timestamps for tracking

### Contact
- Personal information (name, email, phone)
- Company association
- Contact type classification
- Assignment to users
- Address and notes

### Lead
- Potential customer information
- Status tracking (New, Contacted, Qualified, Converted, Closed Lost)
- Source tracking
- Assignment and notes

### Deal
- Sales opportunity tracking
- Stage management (Prospecting to Closed Won/Lost)
- Amount and probability
- Expected close dates
- Priority levels

### Activity
- Task and event management
- Types: Call, Email, Meeting, Task, Note
- Status tracking and completion
- Due dates and assignments
- Links to contacts and deals

## Usage Guide

### Dashboard
- View system statistics and KPIs
- See recent and upcoming activities
- Quick access to create new records
- Lead conversion rate tracking

### Managing Companies
1. Navigate to Companies section
2. Add new companies with detailed information
3. View company details and associated contacts/deals
4. Search and filter companies

### Managing Contacts
1. Add contacts with company associations
2. Categorize by type (Customer, Prospect, Partner, Vendor)
3. Assign to team members
4. Track activities and deals

### Managing Leads
1. Capture leads from various sources
2. Track through qualification process
3. Convert qualified leads to contacts/deals
4. Monitor conversion rates

### Managing Deals
1. Create deals linked to contacts and companies
2. Set deal stages and probability
3. Track deal value and expected close dates
4. Monitor sales pipeline

### Managing Activities
1. Schedule calls, meetings, and tasks
2. Link activities to contacts and deals
3. Track completion status
4. View upcoming activities on dashboard

## Customization

### Styling
- Modify `static/css/custom.css` for custom styling
- Bootstrap 5 classes available throughout
- CSS custom properties for easy theme changes

### Models
- Extend models in `crm/models.py`
- Add custom fields or relationships
- Create and run migrations after changes

### Views & Templates
- Customize views in `crm/views.py`
- Modify templates in `templates/crm/`
- Add new functionality as needed

## API Considerations

This system is designed as a web application with Django views. For API functionality:
- Consider Django REST Framework integration
- Add serializers for model data
- Implement API endpoints for mobile/external access

## Security Features

- Django's built-in CSRF protection
- User authentication required for all views
- SQL injection protection through ORM
- XSS protection in templates

## Performance Optimizations

- Database query optimization with `select_related()`
- Pagination for large datasets
- Efficient search with database indexes
- Static file handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the Django documentation
2. Review the code comments
3. Create an issue in the repository

## Future Enhancements

- Email integration
- Calendar synchronization
- Reporting and analytics
- Mobile responsive improvements
- API development
- Integration with external services
- Advanced workflow automation