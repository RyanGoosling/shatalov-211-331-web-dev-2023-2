import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://std_1846_exam:pa$$w0rd@std-mysql.ist.mospolytech.ru/std_1846_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')