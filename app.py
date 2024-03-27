from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Enquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200))
    opcoes = db.relationship('Opcao', backref='enquete', lazy=True)

class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enquete_id = db.Column(db.Integer, db.ForeignKey('enquete.id'), nullable=False)
    descricao = db.Column(db.String(80), nullable=False)
    votos = db.Column(db.Integer, default=0)

@app.route('/api/enquetes', methods=['POST'])
def criar_enquete():
    if not request.json or not 'titulo' in request.json:
        abort(400)
    enquete = Enquete(titulo=request.json['titulo'], descricao=request.json.get('descricao', ""))
    db.session.add(enquete)
    db.session.commit()
    return jsonify({'enquete': enquete.id}), 201

    # Criar Enquete

@app.route('/api/enquetes', methods=['GET'])
def listar_enquetes():
    enquetes = Enquete.query.all()
    return jsonify({'enquetes': [enquete.id for enquete in enquetes]})

    # Listar Enquetes

@app.route('/api/enquetes/<id>', methods=['GET'])
def obter_detalhes_enquete(id):
    enquete = Enquete.query.get(id)
    if enquete is None:
        abort(404)
    return jsonify({'titulo': enquete.titulo, 'descricao': enquete.descricao})

    # Obter detalhes de uma enquete

@app.route('/api/enquetes/<id>/votar', methods=['POST'])
def votar_opcao_enquete(id):
    if not request.json or not 'opcao_id' in request.json:
        abort(400)
    opcao = Opcao.query.filter_by(id=request.json['opcao_id'], enquete_id=id).first()
    if opcao is None:
        abort(404)
    opcao.votos += 1
    db.session.commit()
    return jsonify({'votos': opcao.votos}), 200

    # Votar em uma opção de enquete

@app.route('/api/enquetes/<id>/resultados', methods=['GET'])
def resultados_enquete(id):
    opcoes = Opcao.query.filter_by(enquete_id=id).all()
    if not opcoes:
        abort(404)
    resultados = {opcao.descricao: opcao.votos for opcao in opcoes}
    return jsonify(resultados)

    # Resultados de uma enquete

@app.route('/api/enquetes/<id>/opcoes', methods=['GET'])
def visualizar_opcoes_enquete(id):
    opcoes = Opcao.query.filter_by(enquete_id=id).all()
    if not opcoes:
        abort(404)
    return jsonify({'opcoes': [opcao.descricao for opcao in opcoes]})

    # Visualizar opções de uma enquete

@app.route('/api/enquetes/<id>/opcoes', methods=['POST'])
def adicionar_opcao_enquete(id):
    if not request.json or not 'descricao' in request.json:
        abort(400)
    opcao = Opcao(enquete_id=id, descricao=request.json['descricao'])
    db.session.add(opcao)
    db.session.commit()
    return jsonify({'opcao': opcao.id}), 201

    # Adicionar a opção em uma enquete

@app.route('/api/enquetes/<id>', methods=['DELETE'])
def deletar_enquete(id):
    enquete = Enquete.query.get(id)
    if enquete is None:
        abort(404)
    db.session.delete(enquete)
    db.session.commit()
    return jsonify({'resultado': True})

    # Deletar enquete

@app.route('/api/enquetes/<id_enquete>/opcoes/<id_opcao>', methods=['DELETE'])
def deletar_opcao_enquete(id_enquete, id_opcao):
    opcao = Opcao.query.filter_by(id=id_opcao, enquete_id=id_enquete).first()
    if opcao is None:
        abort(404)
    db.session.delete(opcao)
    db.session.commit()
    return jsonify({'resultado': True})

    # Deletar uma opção de uma enquete


