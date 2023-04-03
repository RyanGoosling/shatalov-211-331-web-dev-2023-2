from flask import Flask, render_template, request
from flask import make_response

app = Flask(__name__)
application = app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))
    if "name" in request.cookies:
        resp.delete_cookie("name")
    else:
        resp.set_cookie("name", "value")
    return resp

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    answer=''
    error_text=''
    if request.method=='POST':
        try:
            first_num = int(request.form['firstnumber'])
            second_num = int(request.form['secondnumber'])
        except ValueError:
            error_text='Был передан текст. Введите, пожалуйста, число.'
            return render_template('calc.html', answer=answer, error_text=error_text)
        operation = request.form['operation']
        if operation == '+':
            answer = first_num + second_num
        elif operation == '-':
            answer = first_num - second_num
        elif operation == '*':
            answer = first_num * second_num
        elif operation == '/':
            try:
                answer = first_num / second_num
            except ZeroDivisionError:
                error_text = 'На ноль делить нельзя'
    return render_template('calc.html', answer=answer, error_text=error_text)

def phone_filter(phone):
    #может содержать: пробелы, круглые скобки, дефисы, точки, +
    phone = phone.replace(' ','').replace('(','') 
    phone = phone.replace(')','').replace('-','')
    phone = phone.replace('.','').replace('+','')
    return phone

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    result = '8-'
    error = False
    if request.method == 'POST':
        phone = str(request.form['phone'])
        phone = phone_filter(phone)

        if phone.isdigit():
            if len(phone) == 11 and (phone[0] == '8' or phone[0] == '7'):
                result = '-'.join([phone[0], phone[1:4], phone[4:7], phone[7:9], phone[9:11]])
            elif len(phone) == 10:
                result += '-'.join([phone[:3], phone[3:6], phone[6:8], phone[8:]])
            else:
                result = 'Недопустимый ввод. Неверное количество цифр.'
                error = True
        else:
            result = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
            error = True

    return render_template('phone.html', result = result, error = error)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404