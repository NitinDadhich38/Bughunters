import os
import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from io import StringIO

db = SQLAlchemy()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def get_llm_analysis(df):
    if df.empty:
        return {"error": "The uploaded CSV file is empty."}
    summary = (
        "The financial data indicates a stable yet cautious outlook. "
        "Revenue streams appear consistent, but there are early indicators of rising operational costs. "
        "Liquidity remains strong, though attention should be paid to accounts receivable turnover."
    )
    suggestions = [
        {"title": "Cost Optimization Initiative", "suggestion": "...", "impact": "..."},
        {"title": "Accelerate Accounts Receivable Collection", "suggestion": "...", "impact": "..."},
        {"title": "Invest in Supply Chain Technology", "suggestion": "...", "impact": "..."},
        {"title": "Explore Market Diversification", "suggestion": "...", "impact": "..."},
        {"title": "Launch a Digital Transformation Project", "suggestion": "...", "impact": "..."},
    ]
    return {"summary": summary, "suggestions": suggestions}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_secure_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cfo_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        analysis = None
        chart_data = None
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file and file.filename.endswith('.csv'):
                try:
                    s = str(file.read(), 'utf-8')
                    df = pd.read_csv(StringIO(s))
                    llm_analysis = get_llm_analysis(df)
                    analysis = {
                        'summary': df.describe().to_html(classes='table table-striped'),
                        'head': df.head().to_html(classes='table table-striped'),
                        'llm': llm_analysis
                    }
                    if 'Category' in df.columns and 'Amount' in df.columns:
                        chart_df = df.groupby('Category')['Amount'].sum().reset_index()
                        chart_data = {
                            'labels': chart_df['Category'].tolist(),
                            'data': chart_df['Amount'].tolist(),
                        }
                    flash('File successfully analyzed!', 'success')
                except Exception as e:
                    flash(f'Error analyzing file: {e}', 'danger')
            else:
                flash('Please upload a CSV file.', 'danger')
        return render_template('dashboard.html', analysis=analysis, chart_data=chart_data)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
