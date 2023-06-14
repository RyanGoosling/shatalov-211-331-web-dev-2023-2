import os
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import YEAR
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db
from users_policy import UsersPolicy

RATING_WORDS = {
    5: 'Отлично',
    4: 'Хорошо',
    3: 'Удовлетворительно',
    2: 'Неудовлетворительно',
    1: 'Плохо',
    0: 'Ужасно',
}

book_genre = db.Table('book_genre',
                      db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                      db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
                      )

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return '<Genre %r>' % self.name

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    year = db.Column(YEAR, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    rating_sum = db.Column(db.Integer, nullable=False, default=0)
    rating_num = db.Column(db.Integer, nullable=False, default=0)
    background_image_id = db.Column(db.String(100), db.ForeignKey('images.id'))
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())

    genres = db.relationship('Genre', secondary=book_genre, backref='books')#backref: genres.books = books.genres
    bg_image = db.relationship('Image', backref='books')
    reviews = db.relationship('Review', cascade='all, delete', backref='book')

    def __repr__(self):
        return '<Book %r>' % self.name

    @property
    def rating(self):
        if self.rating_num > 0:
            return self.rating_sum / self.rating_num
        return 0
    
    def rating_up(self, n:int):
        self.rating_num += 1
        self.rating_sum += n

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='reviews')

    @property
    def rating_word(self):
        return RATING_WORDS.get(self.rating)

    def __repr__(self):
        return '<Review %r, %r>' % (self.id, self.text[:10])
    
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    role = db.relationship('Role')

    def set_password(self, password:str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password:str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])
    
    @property
    def is_admin(self):
        return self.role.name == 'Администратор'

    @property
    def is_moder(self):
        return (self.role.name == 'Администратор' or self.role.name == 'Модератор')
    
    def can(self, action, record = None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False

    def __repr__(self):
        return '<User %r>' % self.login
    
# flask db init
# flask db migrate -m "comment"
# flask db upgrade

# User.query.all()
# User.query.get(user.id)
# User.query.first()
# User.query.filter_by(login='user').first()
# User.query.filter(User.login=='petrov').first()
# User.query.filter(User.login=='petrov').filter(User.role_id=='1').first() login = 'petrov AND role_id=='1'
# from sqlalchemy import and_, or_, not_
# User.query.filter(or_(User.login=='petrov').filter(User.role_id=='1')).all() login = 'petrov OR role_id=='1'
# query = User.query
# query = query.filter(User.login == 'user')
# query = query.filter(User.role_id == None)
# query.all()
# User.query.filter(not_(User.login.in_(['user', 'petrov']))).limit(10).all()