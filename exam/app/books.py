from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import current_user, login_required
from auth import permission_check
from app import db, app
from models import Book, Genre, Review, History
from tools import ImageSaver, ImageDeleter
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
    recently_books = request.cookies.get('recently_books')
    if recently_books:
        recently_books = recently_books.split(',')
        print('='*30, '\n', recently_books)
        recently_books = list(map(Book.query.get, recently_books))
    print('='*30, '\n', recently_books)
    return render_template('books/index.html',
                           books=books, search_params={},
                           pagination=pagination, recent_books=recently_books)

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
    genres_list = Genre.query.all()
    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()
        imgDel = ImageDeleter(img)
    else:
        flash(f'Выберите обложку для книги', 'warning')
        return render_template('books/new.html',
                           genres=genres_list, book=Book(**params()))
        
    book = Book(**params(), background_image_id=img.id)
    book.short_desc = bleach.clean(book.short_desc)
    genres = request.form.getlist('genres')
    if not genres:
        imgDel.delete(0)
        flash(f'Выставите жанры для книги', 'warning')
        return render_template('books/new.html',
                           genres=genres_list, book=book)
                           
    genres = list(map(Genre.query.get, genres))
    book.genres.extend(genres)
    for key in BOOK_PARAMS:
        if not getattr(book, key):
            imgDel.delete(0)
            flash(f'Заполните все поля книги', 'warning')
            return render_template('books/new.html',
                                   genres=genres_list, book=book)
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
        imgDel.delete(0)
        genres = Genre.query.all()
        return render_template('books/new.html',
                           genres=genres_list, book=book)
    return redirect(url_for('books.index'))


@bp.route('/<int:book_id>')
def show(book_id):
    if not loger(book_id):
        return redirect(url_for('index'))
    book = Book.query.get(book_id)
    user_review = Review()
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id).filter_by(book_id=book_id).first()
    # Просмотр книги (book_id) записывается в куки
    recently_books = request.cookies.get('recently_books')
    if recently_books:
        recently_books = recently_books.split(',')
    else:
        recently_books = []
    print('='*30, '\n', recently_books)
    if str(book_id) in recently_books:
        recently_books.remove(str(book_id))
        recently_books.insert(0, str(book_id))
    else:
        recently_books.insert(0, str(book_id))
    recently_books = recently_books[:5]
    print('='*30, '\n', recently_books)
    recently_books_str = ','.join(recently_books)

    response = make_response(render_template('books/show.html', book=book, review=user_review))
    response.set_cookie('recently_books', recently_books_str)
    return response

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
    try:
        db.session.delete(book)
        imgDel = ImageDeleter(book.bg_image)
        imgDel.delete(1)
        db.session.commit()
        flash(f'Книга "{book.name}" была успешно удалена!', 'success')
    except sa.exc.SQLAlchemyError as exc:
        print('='*30, "\n", exc, "\n", '='*30)
        flash(f'При удалении книги "{book.name}" произошла ошибка', 'danger')
        db.session.rollback()
    return redirect(url_for('books.index'))