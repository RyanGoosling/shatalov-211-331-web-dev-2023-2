from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from auth import permission_check
from app import db, app
from models import Book, Genre, Review
from tools import ImageSaver, Image
import sqlalchemy as sa
import os

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
@permission_check('create')
def new(): #user petrov fedorov stepanov maximov
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
@permission_check('create')
def create():
    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()
        
    book = Book(**params(), background_image_id=img.id)
    genres = request.form.getlist('genres')
    genres = list(map(Genre.query.get, genres))
    book.genres.extend(genres)
    try:
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

    return render_template('books/show.html', book=book,
                           review=user_review)

@bp.route('/<int:book_id>/new review', methods=['POST'])
@login_required
def new_review(book_id): 
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
    return redirect(url_for('books.show', book_id=book_id))

@bp.route('/<int:book_id>/edit')
@permission_check('update')
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    params={'book_id': book_id}

    return render_template('books/edit.html', book=book, 
                           genres=genres, params=params)

@bp.route('/<int:book_id>/update', methods=['POST'])
@permission_check('update')
def update(book_id):
    book = Book.query.get(book_id)
    new_params = params()
    for key, value in new_params.items():
        if value:
            setattr(book, key, value)
    genres = request.form.getlist('genres')
    if genres:
        genres = list(map(Genre.query.get, genres))
        book.genres = genres
    try:
        db.session.commit()
        flash(f'Книга "{book.name}" была успешно изменена!', 'success')

    except sa.exc.SQLAlchemyError as exc:
        print(exc)
        flash(f'При изменении книги "{book.name}" произошла ошибка', 'danger')
        db.session.rollback()
        genres = Genre.query.all()
        return redirect(url_for('books.edit', book_id=book_id))
    return redirect(url_for('books.show', book_id=book_id))

@bp.route('/<int:book_id>/delete', methods=['POST'])
@permission_check('delete')
def delete(book_id):
    book = Book.query.get(book_id)
    books_of_cover = Book.query.filter_by(background_image_id=book.bg_image.id).all()
    len_of_books = len(books_of_cover)
    try:
        db.session.delete(book)
        if len_of_books == 1:
            cover = Image.query.get(book.bg_image.id)
            db.session.delete(cover)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                            cover.storage_filename))
        db.session.commit()
        flash(f'Книга "{book.name}" была успешно удалена!', 'success')
    except sa.exc.SQLAlchemyError as exc:
        print('='*30, "\n", exc, "\n", '='*30)
        flash(f'При удалении книги "{book.name}" произошла ошибка', 'danger')
        db.session.rollback()
    return redirect(url_for('books.index'))