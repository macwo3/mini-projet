import os
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()


app=Flask(__name__)
motdepasse=quote_plus(os.getenv('db_password'))
hostname=os.getenv('hostname')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:{}@{}:5432/appg3'.format(motdepasse,hostname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response


class Etudiant(db.Model):
    __tablename__='etudiants'
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(100), nullable=False) 
    adresse = db.Column(db.String(100), nullable=False) 

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'adresse': self.adresse
    }

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()
db.create_all()


############################################
#
#selectionner un etudiant
#
############################################
@app.route('/etudiants', methods=['GET'])
def liste_etudiants():
    #recuperer la liste des etudiants
    etudiants=Etudiant.query.all()
    etudiants_formated=[et.format() for et in etudiants]
    return jsonify({
        'success':True,
        'total etudiants':len(etudiants),
        'etudiants':etudiants_formated
    })

@app.route('/etudiants/<int:id>')
def selectionner_etudiant(id):
    #requete pour selectionner un etudiant avec sqlalchemy
    etudiant=Etudiant.query.get(id)
    if etudiant is None:
        abort(404)
    else:
        return jsonify({
            'success':True,
            'selected_id':id,
            'etudiant':etudiant.format()
        })

############################################
#
#creer un nouvel etudiant
#
############################################

@app.route('/etudiant', methods=['POST'])
def ajouter_etudiant(id):
    body=request.get_json()#recuperer les données json
    new_nom=body.get('nom', None)
    new_prenom=body.get('prenom', None)
    new_adresse=body.get('adresse', None)
    etudiant=Etudiant(nom=new_nom, prenom=new_prenom, adresse=new_adresse)
    etudiant.insert()
    return jsonify({
        'success': True,
        'Total_etudiants':Etudiant.query.count(),
        'liste':[et.format() for et in Etudiant.query.all()]
    })

    #####################################################"
    # 
    #supprimer etudiant
    #
    ########################################################
    @app.route('/etudiants/<int:id>', methods=['DELETE'])
    def supprimer_etudiant(id):
        etudiant=Etudiant.query.get(id)
        if livre is None:
            abort(404)
        else:
            etudiant.delete()
            return jsonify({
                'success':True,
                'deleted_id':id,
                'etudiant':etudiant.format()

    })

    #############################################
    #
    #Modifier un etudiant
    #
    ######################################################
    @app.route('/etudiants/<int:id>', methods=['PATCH'])
    def modifier_etudiant(id):
        if etudiant is None:
            abort(404)
        else:
            body=request.get_json()
            etudiant=Etudiant.query.get(id)
            etudiant.nom=body.get('nom')
            etudiant.prenom=body.get('prenom')
            etudiant.adresse=body.get('adresse')
            etudiant.update()
            return jsonify({
                'success':True,
                'updated_id':id,
                'etudiant':etudiant.format()
            })

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "succes": False,
        "error":500,
        "message":"Internal server error"
    }),500