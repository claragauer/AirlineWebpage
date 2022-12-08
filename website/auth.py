from flask import Blueprint, render_template, request
from .database import mysql
import re
# store the standard routes for a website where the user can navigate to
auth = Blueprint('auth', __name__)
@auth.route('anmelden', methods = ['POST', 'GET'])
def anmelden():
    return render_template("anmelden.html")


@auth.route('/logout')
def logout():
    return render_template("logout.html")
@auth.route('/registrieren', methods= ['GET', 'POST'])
def registrieren():
    msg = ''
    if request.method == 'POST' and 'vorname' in request.form and 'nachname' in request.form and 'emailAdresse' in request.form and 'passwort' in request.form:
        vorname = request.form['vorname']
        nachname = request.form['nachname']
        emailAdresse= request.form['emailAdresse']
        passwort= request.form['passwort']

        cursor= mysql.get_db().cursor()
        cursor.execute('SELECT * FROM nutzerkonto WHERE emailAdresse = % s', (emailAdresse,))
        konto = cursor.fetchone()
        if konto:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailAdresse):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', passwort):
            msg = 'Passwort must contain only characters and numbers !'
        elif not vorname or not nachname or not emailAdresse or not passwort:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO nutzerkonto VALUES (NULL, % s, % s, % s, % s , "Passagier")', (vorname, nachname, emailAdresse , passwort ))
            mysql.get_db().commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registrieren.html', msg=msg)


