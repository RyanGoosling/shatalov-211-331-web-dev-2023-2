from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from auth import permission_check
from app import db, app
from models import Book, Genre, Review, History
from tools import ImageSaver, Image
import sqlalchemy as sa
import os, bleach, datetime

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 6

BOOK_PARAMS = [
    'name', 'short_desc', 'year', 
    'publisher', 'author', 'pages'
]

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }

def loger(book_id):
    user_id = getattr(current_user, 'id', None)
    today = datetime.date.today()
    count = History.query.filter(History.user_id == user_id, 
                                 sa.func.date(History.created_at) == today
                                 ).count()
    if count >= 10:
        return True
    history = History(user_id=user_id, book_id=book_id)
    try:
        db.session.add(history)
        db.session.commit()
        return True
    except sa.exc.SQLAlchemyError as exc:
        print('='*30, '\n', exc)
        flash(f'При отображении книги произошла ошибка', 'danger')
        db.session.rollback()
        return False


@bp.route('/')
def index():#http://httpbin.org/post
    page = request.args.get('page', 1, type=int)
    # print('='*30, "\n", search_params(), "\n", '='*30)
    books = Book.query.order_by(Book.created_at.desc())
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    return render_template('books/index.html',
                           books=books, search_params={},
                           pagination=pagination)

@bp.route('/popular')
def popular():
    three_months_ago = datetime.datetime.now() - datetime.timedelta(days=3 * 30)
    records = History.query.with_entities(History.book_id
    ).filter(History.created_at >= three_months_ago
    ).group_by(History.book_id).order_by(sa.func.count(History.book_id).desc()
    ).limit(5).all()

    records = list(map(list, records))
    records = sum(records, []) #[[a], [b]] -> [a, b]
    books = []
    for record in records:
        books.append(Book.query.filter_by(id = record).first()) 
    return render_template('books/index.html', books=books)

@bp.route('/new')
@login_required
@permission_check('create')
def new(): #user/pavlov petrov/alexeev fedorov stepanov maximov tarasov danilov
    genres = Genre.query.all()
    return render_template('books/new.html',
                           genres=genres, book={})

@bp.route('/create', methods=['POST'])
@login_required
@permission_check('create')
def create():
    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()
    else:
        flash(f'Выберите обложку для книги', 'warning')
        genres = Genre.query.all()
        return render_template('books/new.html',
                           genres=genres, book=Book(**params()))
        
    book = Book(**params(), background_image_id=img.id)
    book.short_desc = bleach.clean(book.short_desc)
    genres = request.form.getlist('genres')
    if not genres:
        flash(f'Выставите жанры для книги', 'warning')
        genres = Genre.query.all()
        return render_template('books/new.html',
                           genres=genres, book=book)
                           
    genres = list(map(Genre.query.get, genres))
    book.genres.extend(genres)
    try:
        db.session.add(book)
        db.session.commit()
        flash(f'Книга "{book.name}" была успешно добавлена!', 'success')

    except sa.exc.SQLAlchemyError as exc:
        print('='*30, '\n', exc)
        flash(f'При сохранении книги произошла ошибка', 'danger')
        db.session.rollback()
        #После отката проверяем принадлежность обложки к книгам
        #Если обложка не привязана к книге, то удаляем
        book_of_cover = Book.query.filter_by(background_image_id=img.id).all()
        if len(book_of_cover) == 0:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                            img.storage_filename))
            db.session.delete(img)
        db.session.commit()
        genres = Genre.query.all()
        return render_template('books/new.html',
                           genres=genres, book=book)
    return redirect(url_for('books.index'))


@bp.route('/<int:book_id>')
def show(book_id):
    if not loger(book_id):
        return redirect(url_for('index'))
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
        flash(f'Вы уже оставляли отзыв на эту книгу.', 'warning')
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
@login_required
@permission_check('update')
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    params={'book_id': book_id}

    return render_template('books/edit.html', book=book, 
                           genres=genres, params=params)

@bp.route('/<int:book_id>/update', methods=['POST'])
@login_required
@permission_check('update')
def update(book_id):
    book = Book.query.get(book_id)
    new_params = params()
    for key, value in new_params.items():
        if value:
            if key == 'short_desc':
                value = bleach.clean(value)
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
@login_required
@permission_check('delete')
def delete(book_id):
    book = Book.query.get(book_id)
    books_of_cover = Book.query.filter_by(background_image_id=book.bg_image.id).all()
    len_of_books = len(books_of_cover)
    try:
        db.session.delete(book)
        if len_of_books == 1: #Если на обложку ссылается несколько книг, то удалять не надо
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