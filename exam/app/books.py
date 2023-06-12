from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Book, Genre, User, Review
from tools import ImageSaver
import sqlalchemy as sa

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 6

BOOK_PARAMS = [
    'name', 'short_desc', 'year', 
    'publisher', 'author', 'pages'
]

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }


@bp.route('/')
def index():#http://httpbin.org/post
    page = request.args.get('page', 1, type=int)
    # print('='*30, "\n", search_params(), "\n", '='*30)
    books = Book.query
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    return render_template('books/index.html',
                           books=books, search_params={},
                           pagination=pagination)

@bp.route('/new')
def new():
    # d1 = {'last_name': 'Иванов', 'first_name': 'Иван', 'middle_name': 'Иванович', 
    #       'login': 'user', 'role_id': '1'}
    # d2 = {'last_name': 'Петров', 'first_name': 'Петр', 'middle_name': 'Петрович', 
    #       'login': 'petrov', 'role_id': '2'}
    # d3 = {'last_name': 'Фёдоров', 'first_name': 'Фёдор', 'middle_name': 'Фёдорович', 
    #       'login': 'fedorov', 'role_id': '3'}
    # d4 = {'last_name': 'Степанов', 'first_name': 'Степан', 'middle_name': 'Степанович', 
    #       'login': 'stepanov', 'role_id': '3'}
    # d5 = {'last_name': 'Максимов', 'first_name': 'Максим', 'middle_name': 'Максимович', 
    #       'login': 'maximov', 'role_id': '3'}
    # user1 = User(**d1)
    # user1.set_password('qwerty')
    # user2 = User(**d2)
    # user2.set_password('qwerty')
    # user3 = User(**d3)
    # user3.set_password('qwerty')
    # user4 = User(**d4)
    # user4.set_password('qwerty')
    # user5 = User(**d5)
    # user5.set_password('qwerty')
    # db.session.add_all([user1, user2, user3, user4, user5])
    # db.session.commit()
    genres = Genre.query.all()
    return render_template('books/new.html',
                           genres=genres, book={})

@bp.route('/create', methods=['POST'])
def create():
    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()
        
    try:
        book = Book(**params(), background_image_id=img.id)
        genres = request.form.getlist('genres')
        for genre_id in genres:#Добавление сущностей Genre в book (MtM связь)
            book.genres.append(Genre.query.get(genre_id))#других способов найти не смог
        db.session.add(book)
        db.session.commit()
        flash(f'Книга "{book.name}" была успешно добавлена!', 'success')

    except sa.exc.SQLAlchemyError as exc:
        print(exc)
        flash(f'При сохранении книги произошла ошибка', 'danger')
        db.session.rollback()
        genres = Genre.query.all()
        return render_template('books/new.html',
                           genres=genres)
    return redirect(url_for('books.index'))


@bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    user_review = Review()
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id).filter_by(book_id=book_id).first()
    book_reviews = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).limit(5).all()
    return render_template('books/show.html', book=book,
                           review=user_review, book_reviews=book_reviews)

@bp.route('/<int:book_id>/new review', methods=['POST'])
@login_required
def new_review(book_id): #user petrov fedorov stepanov maximov
    user_id = current_user.id
    check_review = Review.query.filter_by(book_id=book_id).filter_by(user_id=user_id).all()
    if check_review:
        flash(f'Вы уже оставляли отзыв на этот курс.', 'warning')
        return redirect(url_for('books.show', book_id=book_id))
    text = request.form['text']
    rating = request.form['rating']
    review = Review(text=text, rating=rating, 
                    book_id=book_id, user_id=user_id)
    try:
        db.session.add(review)
        book = Book.query.get(book_id)
        book.rating_up(int(rating))
        db.session.commit()
        flash(f'Отзыв успешно добавлен', 'success')
    except:
        db.session.rollback()
        flash(f'При сохранении отзыва произошла ошибка', 'success')
    # print(user_id, course_id, text, rating, review)
    return redirect(url_for('book.show', book_id=book_id))

@bp.route('/<int:book_id>/edit')
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    params={'book_id': book_id}

    return render_template('books/edit.html', book=book, 
                           genres=genres, params=params)

@bp.route('/<int:book_id>/update', methods=['POST'])
def update(book_id):
    book = Book.query.get(book_id)
    # try:
    #     book = book(**params())
    #     genres = request.form.getlist('genres')
    #     for genre_id in genres:#Добавление сущностей Genre в book (MtM связь)
    #         book.genres.append(Genre.query.get(genre_id))#других способов найти не смог
    #     db.session.add(book)
    #     db.session.commit()
    #     flash(f'Книга "{book.name}" была успешно добавлена!', 'success')

    # except sa.exc.SQLAlchemyError as exc:
    #     print(exc)
    #     flash(f'При сохранении книги произошла ошибка', 'danger')
    #     db.session.rollback()
    #     genres = Genre.query.all()
    #     return render_template('books/new.html',
    #                        genres=genres)
    return redirect(url_for('books.show', book_id=book_id))