from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'  # Update the path as needed
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'xml', 'docx', 'txt'}

db = SQLAlchemy(app)

# Model for payment requests
class PaymentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unidade = db.Column(db.String(50), nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.String(20), nullable=False)
    data_vencimento = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    dados_pagamento = db.Column(db.String(100), nullable=False)  # Updated to capture 'dados_pgt'
    status = db.Column(db.String(20), default='Pendente')  # Status: Pending, Approved, Denied
    attachments = db.relationship('Attachment', backref='payment_request', lazy=True)

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('payment_request.id'), nullable=False)

# Model for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed passwords in production

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        unidade = request.form['unidade']
        fornecedor = request.form['fornecedor']
        cnpj = request.form['cnpj']
        valor = request.form['valor']
        data_vencimento = request.form['data_vencimento']
        descricao = request.form['descricao']
        dados_pagamento = request.form['dados_pgt']  # Capture 'dados_pgt' field
        files = request.files.getlist('file')  # Get multiple files
        
        # Create a new payment request entry
        new_request = PaymentRequest(
            unidade=unidade,
            fornecedor=fornecedor,
            cnpj=cnpj,
            valor=valor,
            data_vencimento=data_vencimento,
            descricao=descricao,
            dados_pagamento=dados_pagamento  # Store 'dados_pgt'
        )
        db.session.add(new_request)
        
        # Save attached files if any
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_attachment = Attachment(filename=filename, payment_request=new_request)
                db.session.add(new_attachment)

        db.session.commit()
        flash('Payment request submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/requests', methods=['GET', 'POST'])
def requests():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        action = request.form.get('action')

        # Find the request by id
        payment_request = PaymentRequest.query.get(request_id)

        if action == 'approve':
            payment_request.status = 'Aprovado'
        elif action == 'deny':
            payment_request.status = 'Negado'

        db.session.commit()
        flash(f'Request {action}d successfully!', 'success')

    # Fetch all payment requests
    requests = PaymentRequest.query.all()
    return render_template('requests.html', requests=requests)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:  # Use hashed passwords in production
        return redirect(url_for('requests'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('index'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            flash('User already exists', 'danger')
            return redirect(url_for('create_user'))
        
        # Create new user
        new_user = User(username=username, password=password)  # Hash password in production
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_user.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True)
