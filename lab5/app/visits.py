
import io
from flask import render_template, Blueprint, request, send_file
from app import db
from math import ceil
PER_PAGE = 10

bp = Blueprint('visits', __name__, url_prefix='/visits')

def generate_report_file(records, fields):
    csv_content = '№,' + ','.join(fields) + '\n'
    for i, record in enumerate(records):
        values = [str(getattr(record, f, '')) for f in fields]
        csv_content += f'{i+1},' + ','.join(values) + '\n'
    f = io.BytesIO()
    f.write(csv_content.encode('utf-8'))
    f.seek(0)
    return f

@bp.route('/')
def logging():
    page = request.args.get('page', 1, type = int)
    query = ('SELECT visit_logs.*, users.login '
            'FROM users RIGHT JOIN visit_logs ON visit_logs.user_id = users.id '
            'ORDER BY created_at DESC LIMIT %s OFFSET %s')
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query, (PER_PAGE, (page-1)*PER_PAGE))
        logs = cursor.fetchall()

    query = 'SELECT COUNT(*) AS count FROM visit_logs'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        count = cursor.fetchone().count
    
    last_page = ceil(count/PER_PAGE)

    return render_template('visits/logs.html', logs = logs, last_page = last_page, current_page = page)

@bp.route('/stat/pages')
def pages_stat():
    query = 'SELECT path, COUNT(*) as count FROM visit_logs GROUP BY path ORDER BY count DESC;'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        records = cursor.fetchall()
    if request.args.get('download_csv'):
        f = generate_report_file(records, ['path', 'count'])
        return send_file(f, mimetype='text/csv', as_attachment=True, download_name='pages_stat.csv')
    return render_template('visits/pages_stat.html', records=records)

@bp.route('/stat/users')
def users_stat():
    query = ('SELECT users.first_name, users.last_name, users.middle_name, COUNT(visit_logs.id) AS count '
            'FROM users '
            'RIGHT JOIN visit_logs ON users.id = visit_logs.user_id '
            'GROUP BY users.login ORDER BY count DESC;')
    #'SELECT path, login, COUNT(*) as count FROM visit_logs GROUP BY login ORDER BY count DESC;'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        records = cursor.fetchall()
    print(records)
    if request.args.get('download_csv'):
        f = generate_report_file(records, ['fisrt_name', 'last_name', 'count'])
        return send_file(f, mimetype='text/csv', as_attachment=True, download_name='users_stat.csv')
    return render_template('visits/users_stat.html', records=records)