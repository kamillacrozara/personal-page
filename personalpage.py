from flask import Flask
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import datetime
from contextlib import closing

app = Flask(__name__)
#app.config.from_object(__name__)
app.config.from_object('configmodule.DevelopmentConfig')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/fill')
def fill_enter():
    return render_template('add_entries.html')

@app.route('/notes')
def notes():
    cur = g.db.execute('select date, title, text from entries order by id desc')
    
    entries = [dict(date=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('notes.html', entries=entries)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add', methods=['POST'])
def add_entry():
    date = datetime.datetime.today().strftime('%B %d, %Y')
    
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into entries (date, title, text) values (? ,?, ?)',
                 [date, request.form['title'], request.form['text']])
    g.db.commit()
    
    return redirect(url_for('notes'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('fill'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('notes'))

if __name__ == '__main__':
    app.run()