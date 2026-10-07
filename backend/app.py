from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db, init_db
from auth import init_auth, authenticate_user, jwt_required, get_jwt_identity
from models import Employee, Request, Category
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)
init_db(app)
init_auth(app)

# Инициализация категорий
def init_categories():
    if Category.query.count() == 0:
        categories = [
            Category(name='IT', description='Проблемы с компьютерами и ПО'),
            Category(name='HR', description='Вопросы по кадрам'),
            Category(name='Office', description='Офисное оборудование'),
            Category(name='Other', description='Другое')
        ]
        db.session.add_all(categories)
        db.session.commit()

# Аутентификация
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    token = authenticate_user(data['username'], data['password'])
    if token:
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Неверные учетные данные'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if Employee.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400
    
    from auth import hash_password
    employee = Employee(
        username=data['username'],
        password=hash_password(data['password']),
        full_name=data['full_name'],
        email=data['email'],
        role=data.get('role', 'employee')
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({'message': 'Регистрация успешна'}), 201

# Заявки
@app.route('/api/requests', methods=['GET'])
@jwt_required()
def get_requests():
    user_id = get_jwt_identity()
    user = Employee.query.get(user_id)
    
    if user.role == 'admin':
        requests = Request.query.all()
    else:
        requests = Request.query.filter_by(author_id=user_id).all()
    
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'status': r.status,
        'priority': r.priority,
        'created_at': r.created_at.isoformat(),
        'category': r.category.name,
        'author': r.author.full_name,
        'executor': r.executor.full_name if r.executor else None
    } for r in requests])

@app.route('/api/requests', methods=['POST'])
@jwt_required()
def create_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    request_obj = Request(
        title=data['title'],
        description=data['description'],
        category_id=data['category_id'],
        priority=data.get('priority', 'medium'),
        author_id=user_id
    )
    db.session.add(request_obj)
    db.session.commit()
    
    return jsonify({'message': 'Заявка создана', 'id': request_obj.id}), 201

@app.route('/api/requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_request(request_id):
    user_id = get_jwt_identity()
    request_obj = Request.query.get_or_404(request_id)
    
    if request_obj.author_id != user_id:
        return jsonify({'error': 'Нет прав'}), 403
    
    data = request.get_json()
    request_obj.title = data.get('title', request_obj.title)
    request_obj.description = data.get('description', request_obj.description)
    request_obj.priority = data.get('priority', request_obj.priority)
    request_obj.status = data.get('status', request_obj.status)
    
    db.session.commit()
    return jsonify({'message': 'Заявка обновлена'})

@app.route('/api/requests/<int:request_id>', methods=['DELETE'])
@jwt_required()
def cancel_request(request_id):
    user_id = get_jwt_identity()
    request_obj = Request.query.get_or_404(request_id)
    
    if request_obj.author_id != user_id:
        return jsonify({'error': 'Нет прав'}), 403
    
    request_obj.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Заявка отменена'})

# Категории
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

if __name__ == '__main__':
    with app.app_context():
        init_categories()
    app.run(debug=True, port=5000)