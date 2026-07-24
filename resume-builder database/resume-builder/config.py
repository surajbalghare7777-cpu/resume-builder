import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'resume-builder-secret-key-2024')
    
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'resume_builder')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    PHOTO_FOLDER = os.path.join(UPLOAD_FOLDER, 'photos')
    ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    PASSPORT_PHOTO_WIDTH = 150  # pixels for PDF
    PASSPORT_PHOTO_HEIGHT = 200  # pixels for PDF
