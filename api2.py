import os
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
from flask_cors import CORS
from sqlalchemy import null
from enum import unique


load_dotenv()


app=Flask(__name__)
motdepasse=quote_plus(os.getenv('db_password'))
hostname=os.getenv('hostname')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:{}@{}:5432/projet'.format(motdepasse,hostname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response



class Categorie(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer, primary_key=True)
    libelle_categorie=db.Column(db.String(100), nullable=False)
    livres=db.relationship('Livre',backref='categories',lazy=True)


    def __init__(self,libelle_categorie):
        self.libelle_categorie=libelle_categorie

    def format(self):
        return{
        'id': self.id,
        'libelle_categorie': self.libelle_categorie
        
    }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

    def update(self):
        db.session.commit()


#db.create_all()

class Livre(db.Model):
    __tablename__='livres'
    id=db.Column(db.Integer, primary_key=True)
    ISBN=db.Column(db.Integer, unique=True)
    titre=db.Column(db.String(50), nullable=False)
    date_publication = db.Column(db.Date,nullable=False ) 
    auteur = db.Column(db.String(50), nullable=False) 
    editeur = db.Column(db.String(50), nullable=False) 
    categorie_id=db.Column(db.Integer, db.ForeignKey('categories.id'))

    #constructeur du livre
    def __init__(self,ISBN,titre,date_publication,auteur,editeur,categorie_id):
        self.ISBN=ISBN
        self.titre=titre
        self.date_publication=date_publication
        self.auteur=auteur
        self.aditeur=editeur
        self.categorie_id=categorie_id

    def format(self):
        return{
        'id': self.id,
        'ISBN':self.ISBN,
        'titre': self.titre,
        'auteur': self.auteur,
        'editeur': self.editeur,
        'date_publication':self.date_publication 
    }


    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

    def update(self):
        db.session.commit()



db.create_all()


#########################liste des livres##########################

@app.route('/livres', methods=['GET'])
def liste_livres():
    #recuperer la liste des livres
    livres=Livre.query.all()
    livres_formated=[liv.format() for liv in livres]
    return jsonify({
        'success':True,
        'total livres':len(Livre.query.all()),
        'livres':livres_formated
    })

#############################chercher un livre###########################

@app.route('/livres/<int:id>')
def chercher_livre(id):

    livre=Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        return jsonify({
            'success':True,
            'selected_id':id,
            'livre':livre.format()
        })

###########################liste des livres d'une  categorie##################

@app.route('/categories/<int:id>/livres', methods=['GET'])
def liste_categorie():
    #recuperer la liste des livres d'une categorie
    categorie=Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        liste=Livre.query.filter_by(categorie_id=id)
        liste_formated=[liv.format() for liv in liste]
    return jsonify({
        'success':True,
        'selected id':id,
        'livres':liste.query.count()
    })


####################lister une categorie####################




##############################################


#############################chercher une categorie par son id#########################

@app.route('/categories/<int:id>')
def chercher_cat(id):
    categorie=Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        return jsonify({
            'success':True,
            'selected_id':id,
            'categorie':categorie.format()
        })

##############################lister toutes les categories##############################""

@app.route('/categories', methods=['GET'])
def liste_cat():
    categories=Categorie.query.all()
    categories_formated=[et.format() for et in categories]
    return jsonify({
        'success':True,
        'total categories':len(categories),
        'categories':categories_formated
         })


############################supprimer un livre##############################

@app.route('/livres/<int:id>', methods=['DELETE'])
def supprimer_livre(id):
    livre=Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        livre.delete()
        return jsonify({
            'success':True,
            'deleted_id':id,
            'livre':livre.format()

        })

#############################Suprimer une categorie###############################

@app.route('/categorie/<int:id>', methods=['DELETE'])
def supprimer_categorie():
    categorie=Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        categorie.delete()
        return jsonify({
            'success':True,
            'deleted_id':id,
            'livre':categorie.format()

        })

#############Modifier livre###############

@app.route('/livres/<int:id>', methods=['PATCH'])
def modifier_livre(id):
    body=request.get_json()
    livre=Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        
        livre.ISBN=body.get('ISBN',None)
        livre.titre=body.get('titre',None)
        livre.auteur=body.get('auteur',None)
        livre.editeur=body.get('editeur',None)
        livre.date_publication=body.get('date_publication',None)
        livre.categorie_id=body.get('categorie_id')

        

        livre.update()
        return jsonify({
            'success':True,
            'updated_id':id,
            'livre':livre.format()
        })

#############Modifier libellé d'une catégorie ###############

@app.route('/categories/<int:id>', methods=['PATCH'])
def modifier_categorie(id):
    body=request.get_json()
    categorie=Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        categorie.libelle=body.get('libelle')
        categorie.update()
        return jsonify({
            'success':True,
            'updated_id':id,
            'livre':categorie.format()
        })

###############gerer les erreurs#######################

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "succes": False,
        "error":500,
        "message":"Internal server error"
    }),500