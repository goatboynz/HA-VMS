# Visitor Management System - Home Assistant Add-on

A comprehensive visitor management system for Home Assistant that allows you to track visitors with sign-in/out capabilities and a full admin backend.

## Features

### Visitor Management
- **Sign-In/Sign-Out System**: Easy-to-use interface for visitors to sign in and out
- **Visitor Information Tracking**: 
  - First and Last Name (required)
  - Phone Number
  - Email Address
  - Physical Address
  - Business/Company Name
  - Purpose of Visit
  - Photo Upload (optional)

### Admin Backend
- **Dashboard**: Overview with statistics and recent visitors
- **Visitor Management**: View all visitors with detailed information
- **Custom Fields**: Add additional fields dynamically from the admin panel
- **Export Capabilities**: Export visitor data as CSV or Excel spreadsheet
- **Photo Management**: View uploaded visitor photos

### Custom Fields
- Add custom fields from the admin backend
- Support for different field types:
  - Text input
  - Textarea
  - Number input
  - Email input
- Mark fields as required or optional

### Data Export
- **CSV Export**: Export all visitor data as CSV file
- **Excel Export**: Export all visitor data as Excel spreadsheet
- Includes all visitor information and custom field data

## Installation

1. Add this repository to your Home Assistant Add-on Store
2. Install the "Visitor Management System" add-on
3. Configure the add-on (see Configuration section)
4. Start the add-on
5. Access the web interface at `http://your-home-assistant-ip:8080`

## Configuration

```yaml
admin_username: admin          # Admin username for backend access
admin_password: changeme       # Admin password (change this!)
database_path: /data/visitors.db  # Database file location
max_file_size: 10485760       # Maximum file size for photo uploads (10MB)
```

## Usage

### For Visitors
1. Navigate to the main page
2. Fill in your information
3. Optionally upload a photo
4. Click "Sign In"
5. When leaving, go to the "Sign Out" page and select your name

### For Administrators
1. Click "Admin" in the navigation
2. Login with your configured credentials
3. Access the dashboard to view statistics
4. Manage visitors, custom fields, and export data

## Default Credentials

- **Username**: admin
- **Password**: changeme

**⚠️ Important**: Change the default password in the add-on configuration before using in production!

## Support

For issues and feature requests, please visit: https://github.com/goatboynz/HA-VMS

## License

This project is licensed under the MIT License.