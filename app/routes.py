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
    usuario_id = get_jwt_identity()
    print(f"Usuário {usuario_id} está adicionando um livro")
    livro = Livro(
        titulo=data['titulo'],
        autor=data['autor'],
        ano_publicacao=data.get('ano'),
        descricao=data.get('descricao'),
        usuario_id=usuario_id
    )
    db.session.add(livro)
    db.session.commit()
    return jsonify({'msg': 'Livro criado com sucesso'}), 201

@api_bp.route('/livros/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_livro(id):
    try:
        # Garante que o ID do usuário é inteiro
        usuario_id = int(get_jwt_identity())
        livro = Livro.query.get_or_404(id)
        
        # Debug: mostra os IDs para verificação
        print(f"Usuário logado: {usuario_id} (tipo: {type(usuario_id)})")
        print(f"Dono do livro: {livro.usuario_id} (tipo: {type(livro.usuario_id)})")
        
        if int(livro.usuario_id) != usuario_id:
            return jsonify({'msg': 'Apenas o dono pode editar este livro'}), 403

        data = request.json
        livro.titulo = data['titulo']
        livro.autor = data['autor']
        livro.ano_publicacao = data.get('ano')
        livro.descricao = data.get('descricao')
        
        db.session.commit()
        return jsonify({'msg': 'Livro atualizado com sucesso'})
    
    except Exception as e:
        print(f"Erro ao atualizar livro: {str(e)}")
        return jsonify({'msg': 'Erro interno ao atualizar livro'}), 500

@api_bp.route('/livros/<int:id>/pode-editar', methods=['GET'])
@jwt_required()
def verificar_edicao_livro(id):
    livro = Livro.query.get_or_404(id)
    usuario_id = get_jwt_identity()
    
    return jsonify({
        'podeEditar': livro.usuario_id == usuario_id,
        'donoLivro': livro.usuario_id,
        'usuarioAtual': usuario_id
    }), 200

@api_bp.route('/livros/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_livro(id):
    try:
        usuario_id = int(get_jwt_identity())
        livro = Livro.query.get_or_404(id)
        livro_usuario_id = int(livro.usuario_id)

        if livro_usuario_id != usuario_id:
            return jsonify({'msg': 'Apenas o usuário que adicionou o livro pode excluí-lo'}), 403

        db.session.delete(livro)
        db.session.commit()
        return jsonify({'msg': 'Livro excluído com sucesso'})

    except Exception as e:
        return jsonify({'msg': 'Erro interno ao excluir livro'}), 500
    
@api_bp.route('/livros/<int:id>', methods=['GET'])
@jwt_required()
def obter_livro(id):
    livro = Livro.query.get_or_404(id)
    return jsonify({
        'id': livro.id,
        'titulo': livro.titulo,
        'autor': livro.autor,
        'ano': livro.ano_publicacao,
        'descricao': livro.descricao,
        'usuario_id': livro.usuario_id
    })

@api_bp.route('/resenhas', methods=['GET'])
@jwt_required()
def listar_resenhas():
    try:
        resenhas = (db.session.query(Resenha, Usuario.nome)
                    .join(Usuario, Resenha.usuario_id == Usuario.id)
                    .all())
        
        return jsonify([{
            'id': r.Resenha.id,
            'conteudo': r.Resenha.conteudo,
            'nota': r.Resenha.nota,
            'livro_id': r.Resenha.livro_id,
            'usuario_id': r.Resenha.usuario_id,
            'usuario_nome': r.nome  # Nome do usuário
        } for r in resenhas])
    
    except Exception as e:
        print(f"Erro ao buscar resenhas: {str(e)}")
        return jsonify({'msg': 'Erro ao carregar resenhas'}), 500

@api_bp.route('/resenhas', methods=['POST'])
@jwt_required()
def criar_resenha():
    data = request.json
    usuario_id = get_jwt_identity()
    
    nota = int(data['nota'])
    if nota < 0 or nota > 5:
        return jsonify({'msg': 'A nota deve estar entre 0 e 5 estrelas'}), 400
        
    resenha = Resenha(
        conteudo=data['conteudo'],
        nota=nota,
        livro_id=int(data['livro_id']),
        usuario_id=usuario_id
    )
    db.session.add(resenha)
    db.session.commit()
    return jsonify({'msg': 'Resenha criada com sucesso'}), 201

@api_bp.route('/resenhas/<int:id>', methods=['PUT'])
@jwt_required()
def editar_resenha(id):
    try:
        usuario_id = int(get_jwt_identity())
        resenha = Resenha.query.get_or_404(id)

        if int(resenha.usuario_id) != usuario_id:
            return jsonify({'msg': 'Apenas o dono pode editar esta resenha'}), 403

        data = request.json
        nota = int(data['nota'])
        if nota < 0 or nota > 5:
            return jsonify({'msg': 'A nota deve estar entre 0 e 5 estrelas'}), 400

        resenha.conteudo = data['conteudo']
        resenha.nota = nota
        db.session.commit()
        return jsonify({'msg': 'Resenha atualizada com sucesso'})
    
    except Exception as e:
        print(f"Erro ao atualizar resenha: {str(e)}")
        return jsonify({'msg': 'Erro interno ao atualizar resenha'}), 500

@api_bp.route('/resenhas/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_resenha(id):
    try:
        usuario_id = int(get_jwt_identity())
        resenha = Resenha.query.get_or_404(id)
        resenha_usuario_id = int(resenha.usuario_id)

        if resenha_usuario_id != usuario_id:
            return jsonify({'msg': 'Apenas o usuário que criou a resenha pode excluí-la'}), 403

        db.session.delete(resenha)
        db.session.commit()
        return jsonify({'msg': 'Resenha excluída com sucesso'})

    except Exception as e:
        return jsonify({'msg': 'Erro interno ao excluir resenha'}), 500
    
@api_bp.route('/resenhas/<int:id>/pode-editar', methods=['GET'])
@jwt_required()
def verificar_edicao_resenha(id):
    resenha = Resenha.query.get_or_404(id)
    usuario_id = get_jwt_identity()
        
    return jsonify({
        'podeEditar': int(resenha.usuario_id) == int(usuario_id),
        'donoResenha': resenha.usuario_id,
        'usuarioAtual': usuario_id
    }), 200

@api_bp.route('/resenhas/<int:id>', methods=['GET'])
@jwt_required()
def obter_resenha(id):
    resenha = Resenha.query.get_or_404(id)
    return jsonify({
        'id': resenha.id,
        'conteudo': resenha.conteudo,
        'nota': resenha.nota,
        'livro_id': resenha.livro_id,
        'usuario_id': resenha.usuario_id
    })