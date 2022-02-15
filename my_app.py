from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from sqlalchemy import column


app = Flask(__name__)
motdepasse=quote_plus('actuel')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:{}@localhost:5432/appg3'.format(motdepasse)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Etudiant(db.Model):
    __tablename__='etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(100), nullable=False) 
    adresse = db.Column(db.String(100), nullable=False) 
db.create_all()

@app.route ('/')
def get_etudiants():
    etudiants=Etudiant.query.all()
    return render_template('index.html', data=etudiants)

@app.route ('/create')
def afficher():
    etudiants=Etudiant.query.all()
    return render_template('create.html')

@app.route ('/add', methods=['POST','GET'])
def ajouter():
    try:
        if request.method=='GET':
            return render_template('create.html')
        elif request.method=='POST':
            new_nom=request.form.get('nom')
            new_prenom=request.form.get('prenom')
            new_addresse=request.form.get('adresse')
            etudiant=Etudiant(nom=new_nom, prenom=new_prenom, adresse=new_addresse)
            db.session.add(etudiant)
            db.session.commit()
            return redirect(url_for('get_etudiants'))
    except:
        db.session.rollback()
    finally:
        db.session.close()

