from flask import Flask, render_template, redirect, make_response, request
from werkzeug.exceptions import abort

from data import db_session, skills
from data.skills import Skills
from data.users import User
from forms.user import RegisterForm, LoginForm, SkillsForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/main')
def index():
    db_sess = db_session.create_session()
    skills = db_sess.query(Skills).filter(Skills.is_private)
    db_sess.close()
    return render_template("main.html", skills=skills, current_user=current_user)


@app.route('/')
def mainpage():
    return render_template('index.html', current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, current_user=current_user)
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.tel.data)
    if form.is_submitted():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.tel == form.tel.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.tel = form.tel.data
        user.home = form.home.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/about')
def about_us():
    return render_template('about.html', title='О нас', current_user=current_user)


@app.route('/newsletter')
def news():
    return render_template('sub.html', title='О нас', current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
