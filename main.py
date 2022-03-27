from app import app
from flask_db import init_app

if __name__ == '__main__':
    init_app(app)
    app.run()
