"""
Complete database fix script
"""
from app import create_app, db
from app.models import Task
import os
import shutil

def fix_database():
    app = create_app()
    
    print("🔧 Starting complete database fix...")
    
    # Step 1: Remove existing database
    db_path = os.path.join('instance', 'todo.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("🗑️  Removed old database file")
        except Exception as e:
            print(f"⚠️  Could not remove old database: {e}")
    
    # Step 2: Ensure instance directory exists
    instance_dir = 'instance'
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print("📁 Created instance directory")
    
    # Step 3: Create fresh database
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Created database tables")
            
            # Verify table creation
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Created tables: {tables}")
            
            if 'task' not in tables:
                raise Exception("Task table was not created!")
            
            # Add sample data
            sample_tasks = [
                Task(title="Welcome to your To-Do App! 🎉", status="Pending"),
                Task(title="Try changing task status", status="Working"),
                Task(title="Example completed task", status="Done"),
            ]
            
            for task in sample_tasks:
                db.session.add(task)
            
            db.session.commit()
            print("📝 Added sample tasks")
            
            # Verify data
            task_count = Task.query.count()
            print(f"✅ Verified: {task_count} tasks in database")
            
            print("\n🎉 Database fix completed successfully!")
            print("🚀 You can now run: python run.py")
            
        except Exception as e:
            print(f"❌ Error during database creation: {e}")
            db.session.rollback()

if __name__ == '__main__':
    fix_database()