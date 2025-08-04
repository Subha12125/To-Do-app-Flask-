from app import create_app, db
from app.models import Task
import os

app = create_app()

# Production configuration
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1)

with app.app_context():
    db.create_all()
    # Add sample data if empty
    if Task.query.count() == 0:
        sample = Task(title="Welcome to your deployed app! 🎉", status="Pending")
        db.session.add(sample)
        db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)