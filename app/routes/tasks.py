from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task
import traceback

tasks_bp = Blueprint('tasks', __name__) 

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        flash("Please log in to access your tasks.", "warning")
        return redirect(url_for('auth.login'))
    
    try:
        # Try to query tasks with explicit error handling
        tasks = Task.query.order_by(Task.id.desc()).all()
        print(f"✅ Successfully loaded {len(tasks)} tasks")  # Debug log
        return render_template('tasks.html', tasks=tasks)
        
    except Exception as e:
        # Log the detailed error
        print(f"❌ Error in view_tasks: {e}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        
        # Try to create tables if they don't exist
        try:
            db.create_all()
            tasks = Task.query.all()
            flash("Database was repaired automatically.", "info")
            return render_template('tasks.html', tasks=tasks)
        except Exception as create_error:
            print(f"❌ Could not create tables: {create_error}")
            flash("Database error. Please contact administrator.", "danger")
            return render_template('tasks.html', tasks=[])

@tasks_bp.route('/add', methods=['GET', 'POST'])
def add_task():
    if 'user' not in session:
        flash("Please log in to add tasks.", "warning")
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        if title and title.strip():
            try:
                new_task = Task(title=title.strip(), status='Pending')
                db.session.add(new_task)
                db.session.commit()
                flash("Task added successfully!", "success")
                print(f"✅ Added task: {title}")  # Debug log
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error adding task: {e}")
                flash("Error adding task. Please try again.", "danger")
        else:
            flash("Task title cannot be empty.", "warning")
    
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    if 'user' not in session:
        flash("Please log in to manage tasks.", "warning")
        return redirect(url_for('auth.login'))
    
    try:
        task = Task.query.get_or_404(task_id)
        old_status = task.status
        
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        
        db.session.commit()
        print(f"✅ Task {task_id} status: {old_status} → {task.status}")
        flash(f"Task status updated to {task.status}!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error updating task {task_id}: {e}")
        flash("Error updating task. Please try again.", "danger")
    
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user' not in session:
        flash("Please log in to manage tasks.", "warning")
        return redirect(url_for('auth.login'))
    
    try:
        task = Task.query.get_or_404(task_id)
        task_title = task.title
        db.session.delete(task)
        db.session.commit()
        print(f"✅ Deleted task: {task_title}")
        flash("Task deleted successfully!", "info")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error deleting task {task_id}: {e}")
        flash("Error deleting task. Please try again.", "danger")
    
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    if 'user' not in session:
        flash("Please log in to manage tasks.", "warning")
        return redirect(url_for('auth.login'))
    
    try:
        count = Task.query.count()
        Task.query.delete()
        db.session.commit()
        print(f"✅ Cleared {count} tasks")
        flash(f"All {count} tasks cleared successfully!", 'info')
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error clearing tasks: {e}")
        flash("Error clearing tasks. Please try again.", "danger")
    
    return redirect(url_for('tasks.view_tasks'))