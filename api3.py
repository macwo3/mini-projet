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


class Livre(db.Model):
    __tablename__='livres'
    id=db.Column(db.Integer, primary_key=True)
    ISBN=db.Column(db.Integer, unique=True)
    titre=db.Column(db.String(50), nullable=False)
    date_publication = db.Column(db.Date, ) 
    auteur = db.Column(db.String(50), nullable=False) 
    editeur = db.Column(db.String(50), nullable=False) 
    categorie_id=db.column(db.Integer, db.Foreignkey('categories.id'))


    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
        'id': self.id,
        'titre': self.titre,
        'auteur': self.auteur,
        'editeur': self.editeur
    }

    def update(self):
        db.session.commit()

db.create_all()

class Categorie(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer, primary_key=True)
    libelle_categorie=db.Column(db.String(100), nullable=False)
    Livre=db.relationship('Categorie',backref='Livre',lazy='dynamic')

db.create_all()


#########################liste des livres##########################

@app.route('/livres', methods=['GET'])
def liste_livres():
    #recuperer la liste des livres
    livres=Livre.query.all()
    livres_formated=[et.format() for et in livres]
    return jsonify({
        'success':True,
        'total livres':len(livres),
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

@app.route('/categories/<int:id>', methods=['GET'])
def liste_cat():
    #recuperer la liste des livres d'une categorie
    categorie=Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        liste=Livre.query.filter_by(categorie_id=id)
        liste_formated=[et.format() for et in liste]
    return jsonify({
        'success':True,
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
    #recuperer la liste des categories
    categories=Categorie.query.all()
    categories_formated=[et.format() for et in categories]
    return jsonify({
        'success':True,
        'total livres':len(categories),
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
            'deletedted_id':id,
            'livre':livre.format()

        })

#############################Suprimer une categorie###############################

@app.route('/suppr_cat', methods=['POST'])
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
    if livre is None:
        abort(404)
    else:
        body=request.get_json()
        livre=Livre.query.get(id)
        livre.nom=body.get('nom')
        livre.nom=body.get('prenom')
        livre.nom=body.get('adresse')
        livre.update()
        return jsonify({
            'success':True,
            'updated_id':id,
            'livre':livre.format()
        })

#############Modifier libellé d'une catégorie ###############

@app.route('/livres/<int:id>', methods=['PATCH'])
def modifier_categorie(id):
    if categorie is None:
        abort(404)
    else:
        body=request.get_json()
        categorie=Categorie.query.get(id)
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