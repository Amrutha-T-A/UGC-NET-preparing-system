import os

class Config:
    SECRET_KEY = '859d540c6cbb87fb5aedc192a66df8353dbb30a0a868bd9d656c03a44954002e'
    
    # Absolute path to ensure SQLite database is always stored in the correct location
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'net_csa.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
