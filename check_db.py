"""
Database diagnostic script
"""
from app import create_app, db
from app.models import Task
import os

def check_database():
    app = create_app()
    
    with app.app_context():
        print("🔍 Database Diagnostic Report")
        print("=" * 40)
        
        # Check if database file exists
        db_path = os.path.join('instance', 'todo.db')
        if os.path.exists(db_path):
            print(f"✅ Database file exists: {db_path}")
            print(f"📁 File size: {os.path.getsize(db_path)} bytes")
        else:
            print(f"❌ Database file missing: {db_path}")
        
        # Check database connection
        try:
            db.engine.execute("SELECT 1")
            print("✅ Database connection: OK")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return
        
        # Check if tables exist
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Tables found: {tables}")
            
            if 'task' not in tables:
                print("❌ 'task' table missing!")
                return
            else:
                print("✅ 'task' table exists")
        except Exception as e:
            print(f"❌ Error checking tables: {e}")
            return
        
        # Check task count
        try:
            task_count = Task.query.count()
            print(f"📝 Total tasks: {task_count}")
            
            if task_count > 0:
                print("📋 Sample tasks:")
                for task in Task.query.limit(3).all():
                    print(f"   • {task.title} ({task.status})")
        except Exception as e:
            print(f"❌ Error querying tasks: {e}")
            return
        
        print("\n🎉 Database diagnostic completed!")

if __name__ == '__main__':
    check_database()