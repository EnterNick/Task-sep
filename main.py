from flask import Flask, render_template, redirect
from sqlalchemy import or_
from werkzeug.exceptions import abort

from data import db_session
from data.feedbacks import Feedbacks
from data.skills import Skills
from data.users import User
from forms.user import RegisterForm, LoginForm, SkillsForm, EditForm, SubForm, SearchForm, FeedbackForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/main', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        skills = db_sess.query(Skills).filter(or_(Skills.title.contains(form.search.data), Skills.content.contains(form.search.data)))
        db_sess.close()
        return render_template("main.html", skills=skills, current_user=current_user, title='Навыки', form=form)
    db_sess = db_session.create_session()
    skills = db_sess.query(Skills).filter()
    db_sess.close()
    return render_template("main.html", skills=skills, current_user=current_user, title='Навыки', form=form)


@app.route('/')
def mainpage():
    return render_template('index.html', current_user=current_user, title='Главная')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.tel == form.tel.data).first()
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
    return redirect("/login")


@app.route('/profile/<username>')
def profile(username):
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.name == username).first():
        abort(404)
    return render_template('profile.html', current_user=current_user, title='Профиль',
                           user=db_sess.query(User).filter(User.name == username).first())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
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


@login_required
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditForm()
    if form.is_submitted():
        if form.password.data and form.password.data != form.password_again.data:
            return render_template('edit.html', title='Изменение профиля',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == current_user.name).first()
        user.name = form.name.data
        user.home = form.home.data
        if form.password.data:
            user.set_password(form.password.data)
        db_sess.commit()
        return redirect(f'/profile/{user.name}')
    return render_template('edit.html', title='Изменение профиля', form=form, current_user=current_user)


@app.route('/about')
def about_us():
    return render_template('about.html', title='О нас', current_user=current_user)


@app.route('/newsletter', methods=['Get', 'Post'])
def sub():
    form = SubForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == current_user.name).first()
        user.email = form.email.data
        db_sess.commit()
        return redirect('/')
    return render_template('sub.html', title='О нас', current_user=current_user, form=form)


@app.route('/add-skill',  methods=['GET', 'POST'])
@login_required
def add_skills():
    form = SkillsForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        skills = Skills()
        skills.title = form.title.data
        skills.content = form.content.data
        current_user.skills.append(skills)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('skills.html', title='Добавление новости', form=form, current_user=current_user)


@app.route('/advantages')
def advantages():
    return render_template('advantages.html', title='Преимущества', current_user=current_user)


@app.route('/feedbacks', methods=['POST', 'GET'])
def feedbacks():
    db_sess = db_session.create_session()
    feedbacks = db_sess.query(Feedbacks).all()
    form = FeedbackForm()
    if form.is_submitted():
        feedback = Feedbacks()
        feedback.content = form.input.data
        current_user.feedbacks.append(feedback)
        db_sess.merge(feedback)
        form.input.data = ''
    db_sess.commit()
    return render_template('feedbacks.html', title='Отзывы', current_user=current_user, feedbacks=feedbacks, form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
