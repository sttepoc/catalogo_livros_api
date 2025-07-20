from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email já registrado'}), 409

    user = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha_hash=generate_password_hash(data['senha'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Usuario.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.senha_hash, data['senha']):
        token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': token})
    return jsonify({'msg': 'Credenciais inválidas'}), 401