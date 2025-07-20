from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Livro, Resenha, Usuario

api_bp = Blueprint('api', __name__)

@api_bp.route('/livros', methods=['GET'])
@jwt_required()
def listar_livros():
    livros = Livro.query.all()
    return jsonify([{
        'id': l.id,
        'titulo': l.titulo,
        'autor': l.autor,
        'ano': l.ano_publicacao,
        'descricao': l.descricao
    } for l in livros])

@api_bp.route('/livros', methods=['POST'])
@jwt_required()
def criar_livro():
    data = request.json
    livro = Livro(
        titulo=data['titulo'],
        autor=data['autor'],
        ano_publicacao=data['ano'],
        descricao=data['descricao']
    )
    db.session.add(livro)
    db.session.commit()
    return jsonify({'msg': 'Livro criado com sucesso'}), 201

@api_bp.route('/livros/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_livro(id):
    livro = Livro.query.get_or_404(id)
    data = request.json
    livro.titulo = data['titulo']
    livro.autor = data['autor']
    livro.ano_publicacao = data['ano']
    livro.descricao = data['descricao']
    db.session.commit()
    return jsonify({'msg': 'Livro atualizado com sucesso'})

@api_bp.route('/livros/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return jsonify({'msg': 'Livro excluído'})

@api_bp.route('/resenhas', methods=['GET'])
@jwt_required()
def listar_resenhas():
    resenhas = Resenha.query.all()
    return jsonify([{
        'id': r.id,
        'conteudo': r.conteudo,
        'nota': r.nota,
        'livro_id': r.livro_id,
        'usuario_id': r.usuario_id
    } for r in resenhas])

@api_bp.route('/resenhas', methods=['POST'])
@jwt_required()
def criar_resenha():
    data = request.json
    usuario_id = get_jwt_identity()
    resenha = Resenha(
        conteudo=data['conteudo'],
        nota=int(data['nota']),
        livro_id=int(data['livro_id']),
        usuario_id=usuario_id
    )
    db.session.add(resenha)
    db.session.commit()
    return jsonify({'msg': 'Resenha criada com sucesso'}), 201

@api_bp.route('/resenhas/<int:id>', methods=['PUT'])
@jwt_required()
def editar_resenha(id):
    usuario_id = get_jwt_identity()
    resenha = Resenha.query.get_or_404(id)

    if resenha.usuario_id != usuario_id:
        return jsonify({'msg': 'Acesso negado'}), 403

    data = request.json
    resenha.conteudo = data['conteudo']
    resenha.nota = int(data['nota'])
    db.session.commit()
    return jsonify({'msg': 'Resenha atualizada com sucesso'})

@api_bp.route('/resenhas/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_resenha(id):
    usuario_id = get_jwt_identity()
    resenha = Resenha.query.get_or_404(id)

    if resenha.usuario_id != usuario_id:
        return jsonify({'msg': 'Acesso negado'}), 403

    db.session.delete(resenha)
    db.session.commit()
    return jsonify({'msg': 'Resenha excluída com sucesso'})