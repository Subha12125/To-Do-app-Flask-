from app import create_app, db
from app.models import Task
import os

app = create_app()

# Ensure database tables are created
with app.app_context():
    try:
        # Create tables if they don't exist
        db.create_all()
        
        # Check if database file exists
        if os.path.exists('instance/todo.db'):
            print("✅ Database connected successfully!")
        else:
            print("⚠️  Database file created.")
            
        # Optional: Add sample data if no tasks exist
        if Task.query.count() == 0:
            sample_tasks = [
                Task(title="Welcome to your To-Do App! 🎉", status="Pending"),
                Task(title="Try changing task status", status="Working"),
                Task(title="Example completed task", status="Done"),
            ]
            
            for task in sample_tasks:
                db.session.add(task)
            
            db.session.commit()
            print("📝 Sample tasks added!")
            
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == '__main__':
    print("🚀 Starting Flask To-Do App...")
    print("🔐 Login with: admin / 1234")
    print("🌐 Open: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)