import os
from flask import Flask, jsonify, request,abort
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus 
from dotenv import load_dotenv 

load_dotenv()
#Demarage de l'application
app=Flask(__name__)
motdepasse=quote_plus(os.getenv('password'))
hostname=os.getenv('host')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:{}@{}:5432/livre_db'.format(motdepasse,hostname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


#Creation de la classe categorie
class Categorie(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer,primary_key=True)
    libelle_categorie=db.Column(db.String(200),nullable=False)
    livres=db.relationship('Livre', backref='categories' ,lazy=True)

#constructeur de la categorie
    def __init__(self,libelle_categorie):
        self.libelle_categorie=libelle_categorie
         

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format (self):
        return{
            'id':self.id,
            'libelle_categorie':self.libelle_categorie,
         }

db.create_all()



#creation de la calss Livre
class Livre(db.Model):
    __tablename__='livres'
    id=db.Column(db.Integer,primary_key=True)
    isbn=db.Column(db.String(10),unique=True)
    titre=db.Column(db.String(200),nullable=False)
    date_publication=db.Column(db.Date,nullable=False)
    auteur=db.Column(db.String(200),nullable=False)
    editeur=db.Column(db.String(200),nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    #constructeur du livre
    def __init__(self,isbn,titre,date_publication,auteur,editeur,categorie_id):
        self.isbn=isbn
        self.titre=titre
        self.date_publication=date_publication
        self.auteur=auteur
        self.aditeur=editeur
        self.categorie_id=categorie_id
           
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'isbn':self.isbn,
            'titre':self.titre,
            'date_publication':self.date_publication,
            'auteur':self.auteur,
            'editeur':self.editeur,
            'categorie_id':self.categorie_id,
         }

#ajouter un livre
db.create_all()
@app.route('/livres', methods=['POST'])
def add_book():
    try :
        body=request.get_json()
        new_isbn= body.get('isbn', None) 
        new_titre= body.get('titre', None) 
        new_date_publication=body.get('date_publication', None)
        new_auteur=body.get('auteur', None)
        new_editeur= body.get('editeur', None) 
        new_categorie_id= body.get('isbn', None) 
        livre=Livre(isbn=new_isbn, titre=new_titre, date_publication=new_date_publication, auteur=new_auteur, editeur=new_editeur,categorie_id=new_categorie_id)
        livre.insert()
        livres = Livre.query.all()
        livre_formated = [l.format() for l in livres]
        
        return jsonify({
            'created_id': livre.id,
            'success': True,
            'total': len(Livre.query.all()),
            'livres': livre_formated      
        })
    except :
        abort(400) 

#La route qui affiche tous les livres
@app.route('/livres',methods=['GET'])
def get_all_books():
    book=Livre.query.all()
    formated_book=[ l.format() for l in book]

#jsonifier les elements qui retourne un dictionnaire
    return jsonify({ 
        'success':True,
        'livres':formated_book,
        'total':Livre.query.count(),
    })
#Chercher un livre par son id
@app.route('/livres/<int:id>',methods=['GET'])
def get_one_book(id):
    book=Livre.query.get(id)
  
    try:
        if book is None:
            abort(404)
        else:
            return jsonify({
                "success":True,
                "selected_id":id,
                "selected_book":book.format()
            })
    except:
        abort(400)

# Lister la liste des livres d’une catégorie
@app.route('/categories/<int:id>/livres' ,methods=['GET'])
def get_cat_book(id):
    cat=Categorie.query.get(id)

    if cat is None:
        abort(404)
    else:
        liste_livre=Livre.query.filter_by(categorie_id=id)
    livres=[lv.format() for lv in liste_livre]
    return jsonify({
                "success":True,
                "selected_id":id,
                "list_book":livres
            })
#ajouter une categorie
@app.route('/categories', methods=['POST'])
def add_cat():
    #try :
        body=request.get_json()
         
        new_libelle_categorie=body.get('libelle_categorie',None)
        categorie = Categorie(libelle_categorie=new_libelle_categorie)
        categorie.insert()
        cat = Categorie.query.all()
        cat_formated = [c.format() for c in cat]
        
        return jsonify({
            'created_id': categorie.id,
            'success'   : True,
            'total'     : len(Categorie.query.all()),
            'categorie' : cat_formated      
        })
   # except :
        
    #    abort(400) 


#chercher une categorie par son id
@app.route('/categories/<int:id>',methods=['GET'])
def get_one_categorie(id):
    cat=Categorie.query.get(id)
  
    try:
        if cat is None:
            abort(404)
        else:
            return jsonify({
                "success":True,
                "selected_id":id,
                "selected_book":cat.format()
            })
    except:
        abort(400) 


#lister tous les categories
@app.route('/categories',methods=['GET'])
def get_all_categories():
    cat=Categorie.query.all()
    formated_cat=[ c.format() for c in cat]

    return jsonify({ 
        'success':True,
        'categories':formated_cat,
        'total':Categorie.query.count(),
    })

# Supprimer un livre
@app.route('/livres/<int:id>',methods=['DELETE'])
def delete_book(id):
    book=Livre.query.get(id)
    if book is None:
        abort(404)
    else:
        book.delete()
        return jsonify({
            "deleted_id":id,
            "success":True,
            "total":Livre.query.count(),
            "deleted_book":book.format()

        })

#Supprimer une categorie
@app.route('/categories/<int:id>',methods=['DELETE'])
def delete_categorie(id):
    cat=Categorie.query.get(id)
    if cat is None:
        abort(404)
    else:
        cat.delete()
        return jsonify({
            "deleted_id":id,
            "success":True,
            "total":Categorie.query.count(),
            "deleted_categorie":cat.format()

        })

#Modifier les informations d’un livre
@app.route('/livres/<int:id>',methods=['PATCH'])
def update_book(id):
   
    bk=Livre.query.get(id)
    if bk is None:
        abort(404)
    else:
        book=request.get_json()
        bk.isbn=book.get('isbn',None)
        bk.titre=book.get('titre',None)
        bk.date_publication=book.get('date_publication',None)
        bk.editeur=book.get('editeur',None)
        bk.auteur=book.get('auteur',None)
        bk.categorie_id=book.get('categorie_id',None)
     
        if bk.isbn is None or bk.titre is None or bk.date_publication is None or bk.editeur is None or bk.isbn is None or bk.auteur is None or bk.categorie_id is None:
            abort(400)
            
        else:
            book.update()
    
            return jsonify({
                "success":True,
                "updated_id_book":id,
                "new_book":bk.format()

            })

#modifier le libelle d'une categorie
@app.route('/categories/<int:id>',methods=['PATCH'])
def update_cat_lib(id):
    cat=request.get_json()
    ct=Categorie.query.get(id)
    ct.libelle_categorie=cat.get('libelle_categorie',None)

    if ct is None:
        abort(404)
        
    else:
        cat.update()
 
        return jsonify({
            "success":True,
            "updated_libelle_categorie":id,
            "new_categorie":cat.format(),

        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success'  :  False,
        'error'    : 404,
        'message'  : 'Not found',
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success'  : False,
        'error'    : 400,
        'Message'  : 'Bad request'
    }), 400

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "succes": False,
        "error":500,
        "message":"Internal server error"
    }),500
    
