#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd
from PIL import Image
import io
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme')
DATABASE_PATH = os.environ.get('DATABASE_PATH', '/data/visitors.db')
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 10485760))
UPLOAD_FOLDER = '/data/uploads'

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create visitors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            address TEXT,
            business_name TEXT,
            purpose_of_visit TEXT,
            photo_path TEXT,
            sign_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sign_out_time TIMESTAMP,
            status TEXT DEFAULT 'signed_in',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create custom fields table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT NOT NULL UNIQUE,
            field_type TEXT NOT NULL,
            is_required BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create visitor custom data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitor_custom_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id INTEGER,
            field_name TEXT,
            field_value TEXT,
            FOREIGN KEY (visitor_id) REFERENCES visitors (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main visitor sign-in page"""
    conn = get_db_connection()
    custom_fields = conn.execute('SELECT * FROM custom_fields ORDER BY field_name').fetchall()
    conn.close()
    return render_template('index.html', custom_fields=custom_fields)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    """Handle visitor sign-in"""
    try:
        conn = get_db_connection()
        
        # Handle photo upload
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                photo_path = os.path.join(UPLOAD_FOLDER, filename)
                
                # Resize and save image
                image = Image.open(file.stream)
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                image.save(photo_path, optimize=True, quality=85)
        
        # Insert visitor record
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visitors (first_name, last_name, phone_number, email, address, 
                                business_name, purpose_of_visit, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form.get('first_name'),
            request.form.get('last_name'),
            request.form.get('phone_number'),
            request.form.get('email'),
            request.form.get('address'),
            request.form.get('business_name'),
            request.form.get('purpose_of_visit'),
            photo_path
        ))
        
        visitor_id = cursor.lastrowid
        
        # Handle custom fields
        custom_fields = conn.execute('SELECT * FROM custom_fields').fetchall()
        for field in custom_fields:
            field_value = request.form.get(f'custom_{field["field_name"]}')
            if field_value:
                cursor.execute('''
                    INSERT INTO visitor_custom_data (visitor_id, field_name, field_value)
                    VALUES (?, ?, ?)
                ''', (visitor_id, field["field_name"], field_value))
        
        conn.commit()
        conn.close()
        
        flash('Successfully signed in! Welcome!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error signing in: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/sign_out')
def sign_out_page():
    """Sign-out page"""
    conn = get_db_connection()
    active_visitors = conn.execute('''
        SELECT * FROM visitors 
        WHERE status = 'signed_in' 
        ORDER BY sign_in_time DESC
    ''').fetchall()
    conn.close()
    return render_template('sign_out.html', visitors=active_visitors)

@app.route('/sign_out/<int:visitor_id>', methods=['POST'])
def sign_out(visitor_id):
    """Handle visitor sign-out"""
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE visitors 
            SET sign_out_time = CURRENT_TIMESTAMP, status = 'signed_out'
            WHERE id = ?
        ''', (visitor_id,))
        conn.commit()
        conn.close()
        
        flash('Successfully signed out!', 'success')
        return redirect(url_for('sign_out_page'))
        
    except Exception as e:
        flash(f'Error signing out: {str(e)}', 'error')
        return redirect(url_for('sign_out_page'))

@app.route('/admin')
def admin_login():
    """Admin login page"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Handle admin login"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    # Get statistics
    total_visitors = conn.execute('SELECT COUNT(*) as count FROM visitors').fetchone()['count']
    active_visitors = conn.execute('SELECT COUNT(*) as count FROM visitors WHERE status = "signed_in"').fetchone()['count']
    today_visitors = conn.execute('''
        SELECT COUNT(*) as count FROM visitors 
        WHERE DATE(sign_in_time) = DATE('now')
    ''').fetchone()['count']
    
    # Get recent visitors
    recent_visitors = conn.execute('''
        SELECT * FROM visitors 
        ORDER BY sign_in_time DESC 
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_visitors=total_visitors,
                         active_visitors=active_visitors,
                         today_visitors=today_visitors,
                         recent_visitors=recent_visitors)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=False)@app.route('
/admin/visitors')
def admin_visitors():
    """Admin visitors list"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    visitors = conn.execute('''
        SELECT * FROM visitors 
        ORDER BY sign_in_time DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin_visitors.html', visitors=visitors)

@app.route('/admin/custom_fields')
def admin_custom_fields():
    """Admin custom fields management"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    custom_fields = conn.execute('SELECT * FROM custom_fields ORDER BY field_name').fetchall()
    conn.close()
    
    return render_template('admin_custom_fields.html', custom_fields=custom_fields)

@app.route('/admin/add_custom_field', methods=['POST'])
def add_custom_field():
    """Add custom field"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO custom_fields (field_name, field_type, is_required)
            VALUES (?, ?, ?)
        ''', (
            request.form.get('field_name'),
            request.form.get('field_type'),
            request.form.get('is_required') == 'on'
        ))
        conn.commit()
        conn.close()
        
        flash('Custom field added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding custom field: {str(e)}', 'error')
    
    return redirect(url_for('admin_custom_fields'))

@app.route('/admin/delete_custom_field/<int:field_id>')
def delete_custom_field(field_id):
    """Delete custom field"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        conn = get_db_connection()
        # Get field name first
        field = conn.execute('SELECT field_name FROM custom_fields WHERE id = ?', (field_id,)).fetchone()
        if field:
            # Delete associated data
            conn.execute('DELETE FROM visitor_custom_data WHERE field_name = ?', (field['field_name'],))
            # Delete field
            conn.execute('DELETE FROM custom_fields WHERE id = ?', (field_id,))
            conn.commit()
            flash('Custom field deleted successfully!', 'success')
        conn.close()
    except Exception as e:
        flash(f'Error deleting custom field: {str(e)}', 'error')
    
    return redirect(url_for('admin_custom_fields'))

@app.route('/admin/export/csv')
def export_csv():
    """Export visitors data as CSV"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        conn = get_db_connection()
        
        # Get all visitors with custom data
        visitors = conn.execute('''
            SELECT v.*, GROUP_CONCAT(vcd.field_name || ': ' || vcd.field_value, '; ') as custom_data
            FROM visitors v
            LEFT JOIN visitor_custom_data vcd ON v.id = vcd.visitor_id
            GROUP BY v.id
            ORDER BY v.sign_in_time DESC
        ''').fetchall()
        
        conn.close()
        
        # Convert to DataFrame
        df = pd.DataFrame([dict(row) for row in visitors])
        
        # Create CSV file
        csv_path = '/data/visitors_export.csv'
        df.to_csv(csv_path, index=False)
        
        return send_file(csv_path, as_attachment=True, download_name=f'visitors_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
    except Exception as e:
        flash(f'Error exporting CSV: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/export/excel')
def export_excel():
    """Export visitors data as Excel"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        conn = get_db_connection()
        
        # Get all visitors with custom data
        visitors = conn.execute('''
            SELECT v.*, GROUP_CONCAT(vcd.field_name || ': ' || vcd.field_value, '; ') as custom_data
            FROM visitors v
            LEFT JOIN visitor_custom_data vcd ON v.id = vcd.visitor_id
            GROUP BY v.id
            ORDER BY v.sign_in_time DESC
        ''').fetchall()
        
        conn.close()
        
        # Convert to DataFrame
        df = pd.DataFrame([dict(row) for row in visitors])
        
        # Create Excel file
        excel_path = '/data/visitors_export.xlsx'
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        return send_file(excel_path, as_attachment=True, download_name=f'visitors_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
        
    except Exception as e:
        flash(f'Error exporting Excel: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/visitor/<int:visitor_id>')
def admin_visitor_detail(visitor_id):
    """Admin visitor detail view"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    visitor = conn.execute('SELECT * FROM visitors WHERE id = ?', (visitor_id,)).fetchone()
    custom_data = conn.execute('''
        SELECT field_name, field_value FROM visitor_custom_data WHERE visitor_id = ?
    ''', (visitor_id,)).fetchall()
    conn.close()
    
    if not visitor:
        flash('Visitor not found', 'error')
        return redirect(url_for('admin_visitors'))
    
    return render_template('admin_visitor_detail.html', visitor=visitor, custom_data=custom_data)

@app.route('/photo/<int:visitor_id>')
def get_photo(visitor_id):
    """Serve visitor photo"""
    conn = get_db_connection()
    visitor = conn.execute('SELECT photo_path FROM visitors WHERE id = ?', (visitor_id,)).fetchone()
    conn.close()
    
    if visitor and visitor['photo_path'] and os.path.exists(visitor['photo_path']):
        return send_file(visitor['photo_path'])
    else:
        # Return a default placeholder image or 404
        return '', 404