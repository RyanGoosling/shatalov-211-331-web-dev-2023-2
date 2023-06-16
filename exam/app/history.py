from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import current_user, login_required
from auth import permission_check
from app import db, app
from models import History
import sqlalchemy as sa
import io, datetime

bp = Blueprint('history', __name__, url_prefix='/history')

PER_PAGE = 10

@bp.route('/users activity')
@login_required
@permission_check('show_log')
def activity():
    page = request.args.get('page', 1, type=int)
    records = History.query.order_by(History.created_at.desc())
    if request.args.get('download_csv'):
        records = records.all()
        fields = ['ФИО', 'Книга', 'Создано']
        csv_content = '№=' + '='.join(fields) + '\n'
        for i, record in enumerate(records):
            values = [str(getattr(record.user, 'full_name', 'Неаутентифицированный пользователь')), 
                      str(record.book.name), str(record.created_at)]
            csv_content += f'{i+1}=' + '='.join(values) + '\n'
        f = io.BytesIO()
        f.write(csv_content.encode('utf-8'))
        f.seek(0)
        today = datetime.date.today()
        return send_file(f, mimetype='text/csv', as_attachment=True, 
                         download_name='activity_'+str(today)+'.csv')
    else:
        pagination = records.paginate(page, PER_PAGE)
        records = pagination.items
    return render_template('history/activity.html', 
                           records=records, pagination=pagination,
                           search_params={})

@bp.route('/books stat')
@login_required
@permission_check('show_log')
def books_stat():
    page = request.args.get('page', 1, type=int)
    records = History.query.with_entities(History.book_id, 
    sa.func.count(History.book_id).label('count')
    ).filter(History.user_id.isnot(None)).group_by(History.book_id
    ).order_by(sa.desc('count'))
    #Запрос вернёт лист <class 'sqlalchemy.engine.row.Row'>
    # внутри (book_id, count), надо привести к <History>, count - 46-48 строки

    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from:
        records = records.filter(History.created_at >= date_from)
    if date_to: #дата берётся до "дата" 00:00
        date_to_next = datetime.datetime.strptime(date_to, "%Y-%m-%d") + datetime.timedelta(days=1)
        records = records.filter(History.created_at <= date_to_next)
    search_params={'date_from': date_from, 'date_to': date_to}

    if request.args.get('download_csv'):
        records = records.all()
    else:
        pagination = records.paginate(page, PER_PAGE)
        records = pagination.items
    print('='*30, '\n', records)
    records = list(map(list, records))
    for record in records:
        record[0] = History.query.filter_by(book_id = record[0]).first()
    print('='*30, '\n', records)
    today = datetime.date.today()
    if request.args.get('download_csv'):
        fields = ['Книга', 'Количество просмотров']
        csv_content = '№=' + '='.join(fields) + '\n'
        for i, record in enumerate(records):
            values = [str(record[0].book.name), str(record[1])]
            csv_content += f'{i+1}=' + '='.join(values) + '\n'
        f = io.BytesIO()
        f.write(csv_content.encode('utf-8'))
        f.seek(0)
        return send_file(f, mimetype='text/csv', as_attachment=True, 
                         download_name='books_stat_'+str(today)+'.csv')
    return render_template('history/books_stat.html', 
                           records=records, pagination=pagination,
                           search_params=search_params, today=today)