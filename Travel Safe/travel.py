import sqlite3
import os

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from qrtools import QR
from contextlib import closing
from werkzeug import secure_filename
from datetime import datetime
import urllib2
import cookielib
from getpass import getpass
import sys
import msg

# configuration
DATABASE = 'travel.db'
DEBUG = True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'svg'])

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('TRAVEL_SETTINGS', silent=True)



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
	
		
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
		
@app.route('/')
def landing():
    if session.get('id'):
        return redirect(url_for('homepage'))
    return render_template('main.html')

@app.route('/friend')	
def friend():
    if not session.get('id'):
        return redirect(url_for('landing'))
    else:
	    
		#query=g.db.execute('select p_num from users where password = ?',[request.form['pw']])
		check = g.db.execute('select dataa from vehicle where p_num = ?',[session.get('id')])    
		
		veh = check.fetchall()
		
        
		return render_template('myFriend.html', veh=veh)	
	    
		return 'ok'
	
@app.route('/home')
def homepage():
    if not session.get('id'):
        return redirect(url_for('landing'))
    sel = g.db.execute('select * from friends where p_num = ?',[session.get('id')])
    entries = [dict(num = row[2]) for row in sel.fetchall()]
    return render_template('homet.html', entries=entries)
	
@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user = g.db.execute('select * from users where p_num = ? and password = ?',[request.form['pn'],request.form['pw']])
        friend = g.db.execute('select * from friends where f_num = ?',[request.form['pn']])
        ct = 0
        for rel in friend.fetchall():
            f_u = g.db.execute('select * from users where p_num = ? and password = ?',[rel[1],request.form['pw']])
            if len(f_u.fetchall())>0:
                ct = 1
        if len(user.fetchall())==0 and ct == 0:
            error = 'Invalid Phone Number OR Password, Try Again'
        else:
            session['id'] = request.form['pn']
            
            if ct == 1:
                    return redirect(url_for('friend'))
            return redirect(url_for('homepage'))
    return error
	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
		   

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return uploaded(file)
			#if filename.decode():
			#		list= filename.data.split(':')
			#		g.db.execute('insert into details (id,plate,ph) values(?,?,?)',[list[0],list[1],list[2]])
			#		g.db.commit()
					
		    #return redirect( url_for('landing') )
            #return redirect(url_for('uploaded', filename=filename))
        else:
            error = "Sorry something went wrong"
    return error
	

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user = g.db.execute('select * from users where p_num = ?',[request.form['pn']])
        if len(user.fetchall())>0:
            error = 'Phone Number already use'
        else:
            g.db.execute('insert into users (p_num,password) values (?,?)',[request.form['pn'],request.form['pw']])
            g.db.execute('insert into friends (p_num,f_num) values (?,?)',[request.form['pn'],request.form['fn']])
            g.db.commit()
            return redirect(url_for('landing'))
    return error

@app.route('/add_friend', methods = ['GET', 'POST'])	
def add_friend():
    error = None
    if request.method == 'POST':
        friend = g.db.execute('select * from friends where p_num = ? and f_num = ?',[session.get('id'),request.form['fn']])
        if len(friend.fetchall())>0:
            error = 'Friend already added'
        else:
            g.db.execute('insert into friends (p_num,f_num) values (?,?)',[session.get('id'),request.form['fn']])
            g.db.commit()
            return redirect(url_for('homepage'))
    return error
	
@app.route('/uploaded')
def uploaded(file):
		from qrtools import QR
		myCode = QR(filename=file)
		if myCode.decode():
			print myCode.data
			g.db.execute('insert into vehicle (p_num,dataa) values(?,?)',[session.get('id'),myCode.data])
			g.db.commit()
			return redirect(url_for('landing'))
		
		return 'Something went wrong'
    
@app.route('/pass', methods = ['GET', 'POST'])
def password():
    error = None
    if request.method == 'POST':
        if request.form['pw'] == request.form['cpw']:
            g.db.execute('update users set password = ? where p_num = ?',[request.form['pw'],session.get('id')])
            g.db.commit()
            return redirect(url_for('homepage'))
        else:
            error = 'Passwords do not match'
    return error

@app.route('/checkin/')	
#@app.route('/<p_num>')
def checkin():

    if not session.get('id'):
        return redirect(url_for('landing'))
    else:
	    
		check = g.db.execute('select dataa from vehicle where p_num=?',[session.get('id')])
		veh = check.fetchall()
		
        
		return render_template('myCheck.html', veh = veh)	
	    
		return 'ok'

@app.route('/message')	
def message():
    msg.message1()
    return redirect(url_for('homepage'))	 
	
@app.route('/map')	
def map():
    
    return render_template('geo.html')	 

@app.route('/mapimg')	
def mapimg():
    
    return render_template('geom.html')	 

	
@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('landing'))
	
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port= port)