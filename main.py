    from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from data.users import User
from data.doctors import Doctor
from data.peoples import People
from data.records import Record
from data.login_form import LoginForm
from data.reg_form import RegisterForm
from data.adddoctor_form import RegDocForm
from data.addtime_form import AddTimeForm
from data.addrec_form import AddRecForm
import datetime
from data import db_session

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'almed_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html', title='Алмед. Медицинский центр')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', form=form, message='Неправильный логин или пароль')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пароли отличаются')
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Email занят другим пользователем')
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        people = People(
            surname=form.fam.data,
            name=form.name.data,
            fname=form.fname.data,
            birth=form.birth.data,
            email=form.email.data,
            polis=form.polis.data
        )
        session.add(user)
        session.add(people)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/admblock', methods=['GET', 'POST'])
@login_required
def admblock():
    session = db_session.create_session()
    doctors = session.query(Doctor).all()
    peoples = session.query(People).all()
    records = session.query(Record).all()
    names = {people.id: (people.surname, people.name, people.fname) for people in peoples}
    names.update({doc.id: (doc.surname, doc.name, doc.fname) for doc in doctors})

    form = RegDocForm()
    form2 = AddTimeForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('admblock.html', title='Администрирование', form=form,
                                   form2=form2,
                                   doctors=doctors, names=names, records=records,
                                   message='Пароли отличаются')
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('admblock.html', title='Администрирование', form=form,
                                   form2=form2,
                                   doctors=doctors, names=names, records=records,
                                   message='Email занят другим пользователем')
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        doctor = Doctor(
            surname=form.fam.data,
            name=form.name.data,
            fname=form.fname.data,
            profile=form.profile.data,
            email=form.email.data,
        )
        session.add(user)
        session.add(doctor)
        session.commit()
        doctors = session.query(Doctor).all()
    return render_template('admblock.html', title='Администрирование', form=form, form2=form2,
                           doctors=doctors, names=names, records=records)


@app.route('/admblock2', methods=['GET', 'POST'])
@login_required
def admblock2():
    session = db_session.create_session()
    doctors = session.query(Doctor).all()
    form = RegDocForm()
    form2 = AddTimeForm()
    if request.method == 'POST':
        num = request.form['doctor']
        time = datetime.datetime.combine(form2.date.data, form2.time1.data)
        d = datetime.timedelta(minutes=30)
        while time < datetime.datetime.combine(form2.date.data, form2.time2.data):
            record = Record(
                doc_id=doctors[int(num) - 1].id,
                people_id=None,
                date=form2.date.data,
                time=time.time(),
            )
            time += d
            session.add(record)
            session.commit()
    return redirect('/admblock')


@app.route('/docs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def docs_delete(id):
    session = db_session.create_session()
    doctor = session.query(Doctor).filter(Doctor.id == id).first()
    if doctor and current_user.email == "admin@admin.ru":
        user = session.query(User).filter(User.email == doctor.email).first()
        session.delete(doctor)
        session.delete(user)
        session.commit()
    else:
        abort(404)
    return redirect('/admblock')


@app.route('/recs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def recs_delete(id):
    session = db_session.create_session()
    record = session.query(Record).filter(Record.id == id).first()
    if record and current_user.email == "admin@admin.ru":
        user = session.query(Record).filter(Record.id == id).first()
        session.delete(record)
        session.commit()
    else:
        abort(404)
    return redirect('/admblock')


@app.route('/addrec', methods=['GET', 'POST'])
@login_required
def addrec():
    form = AddRecForm()
    if request.method == 'POST':
        session = db_session.create_session()
        record = session.query(Record).filter(Record.people_id == None).all()
        rec = session.query(Record).filter(Record.id == record[int(form.record.data) - 1].id).first()
        rec.people_id = current_user.id
        session.commit()
        return redirect('/')
    session = db_session.create_session()
    record = session.query(Record).filter(Record.people_id == None).all()
    doctors = session.query(Doctor).all()
    peoples = session.query(People).all()
    names = {doc.id: (doc.surname, doc.name, doc.fname, doc.profile) for doc in doctors}
    return render_template('addrec.html', title='Запись к врачу', form=form, records=record,
                           name=names)


@app.route('/viewrec', methods=['GET', 'POST'])
@login_required
def viewrec():
    session = db_session.create_session()
    record = session.query(Record).filter(Record.people_id == current_user.id).all()
    doctors = session.query(Doctor).all()
    peoples = session.query(People).all()
    names = {doc.id: (doc.surname, doc.name, doc.fname, doc.profile) for doc in doctors}
    return render_template('viewrec.html', title='Просмотр записей', views=record,
                           name=names)


@app.route('/rec_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def rec_delete(id):
    session = db_session.create_session()
    record = session.query(Record).filter(Record.id == id).first()
    if record and current_user.id == record.people_id:
        record.people_id = None
        session.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/almed.sqlite")
    app.run(port=8000, debug=True)


if __name__ == '__main__':
    main()