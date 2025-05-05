import sys
from os.path import abspath, dirname

# Add project root to Python path
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
