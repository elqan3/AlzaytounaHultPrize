from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =======================
# Database Model
# =======================
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100))
    leader_name = db.Column(db.String(100))
    leader_college = db.Column(db.String(100))
    member2_name = db.Column(db.String(100))
    member2_college = db.Column(db.String(100))
    member3_name = db.Column(db.String(100))
    member3_college = db.Column(db.String(100))
    member4_name = db.Column(db.String(100))
    member4_college = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    reason = db.Column(db.Text)

# =======================
# Forms
# =======================
class RegistrationForm(FlaskForm):
    team_name = StringField('اسم الفريق', validators=[DataRequired()])
    leader_name = StringField('العضو الأول (القائد)', validators=[DataRequired()])
    leader_college = StringField('كلية العضو الأول', validators=[DataRequired()])
    member2_name = StringField('العضو الثاني', validators=[DataRequired()])
    member2_college = StringField('كلية العضو الثاني', validators=[DataRequired()])
    member3_name = StringField('العضو الثالث', validators=[DataRequired()])
    member3_college = StringField('كلية العضو الثالث', validators=[DataRequired()])
    member4_name = StringField('العضو الرابع', validators=[DataRequired()])
    member4_college = StringField('كلية العضو الرابع', validators=[DataRequired()])
    phone = StringField('رقم الهاتف', validators=[DataRequired()])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    reason = TextAreaField('لماذا تريد المشاركة؟', validators=[DataRequired()])
    submit = SubmitField('تسجيل')

class AdminLoginForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired()])
    password = PasswordField('كلمة السر', validators=[DataRequired()])
    submit = SubmitField('دخول')

# =======================
# Routes
# =======================
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        reg = Registration(**form.data)
        db.session.add(reg)
        db.session.commit()
        flash('تم إرسال التسجيل بنجاح!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.username.data == 'elqantri3' and form.password.data == '123456elqan3':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        flash('اسم المستخدم أو كلمة السر خاطئة', 'danger')
    return render_template('admin_login.html', form=form)

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    registrations = Registration.query.all()
    return render_template('admin.html', registrations=registrations)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('admin_login'))

with app.app_context():
    db.create_all()
