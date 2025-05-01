# Task Management System

A Django-based task management system with user roles (SuperAdmin, Admin, User) and JWT authentication.

## Features

- **User Management**
  - Three user roles: SuperAdmin, Admin, User
  - User registration with email verification
  - Admin/SuperAdmin can manage users and tasks
- **Task Management**
  - Create, read, update, delete tasks
  - Task status tracking (Pending, In Progress, Completed)
  - Completion reports and worked hours tracking
- **Authentication**
  - JWT token-based authentication
  - Role-based access control
- **Admin Panel**
  - Dashboard with statistics
  - User and task management interfaces

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task_management.git
   cd task_management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
   ```bash
   POST /api/token/ - Obtain JWT tokens
   ```
   ```bash
   POST /api/token/refresh/ - Refresh JWT token
   ```
### Users
   ```bash
   POST /api/users/register/ - Register a new user
   ```
### Tasks
   ```bash
   GET /api/tasks/ - List tasks assigned to current user
   ```
   ```bash
   PATCH /api/tasks/<id>/ - Update a task
   ```
   ```bash
   GET /api/tasks/<id>/report/ - View task report (Admin/SuperAdmin only)
   ```
## Admin Panel Routes

- `/admin-panel/login/` - Admin login page
- `/admin-panel/` - Admin dashboard  
- `/admin-panel/users/` - User management
- `/admin-panel/tasks/` - Task management

## User Roles

### SuperAdmin
- Full access to all features
- Can create/edit/delete all users and tasks
- Can view all reports

### Admin
- Can manage their assigned users
- Can create/edit/delete tasks for their users  
- Can view reports for their users' tasks

### User
- Can view and update their own tasks
- Can submit completion reports

## Models

### CustomUser
Extends Django's AbstractUser with additional fields:
- `role` (SuperAdmin/Admin/User)
- `managed_by` (reference to Admin/SuperAdmin)

### Task
Fields include:
- `title`, `description`
- `assigned_to` (User)
- `due_date`, `status` (Pending/In Progress/Completed)
- `completion_report`, `worked_hours`
- `created_by`, `created_at`, `updated_at`

## Permissions

### API Permissions
- `IsAuthenticated` - For basic task access
- `IsAdminOrSuperAdmin` - For report viewing

### Admin Panel Permissions
- `superadmin_required` - For user management
- `admin_or_superadmin_required` - For task management

## Templates (Admin Panel)
- Login page
- Dashboard with statistics
- User list/create/edit/delete
- Task list/create/edit/delete  
- Task report view

## Configuration
The project uses Django's default settings with these additions:
- Custom user model: `users.CustomUser`
- JWT authentication
- Static and media file handling in development

## Dependencies
- Django
- Django REST framework  
- djangorestframework-simplejwt
- Python 3.x







