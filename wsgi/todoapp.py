from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, abort
 
app = Flask(__name__)
 
app.config.from_pyfile('todo.cfg')
db = SQLAlchemy(app)
 
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    content = db.Column(db.String(60))
    done = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
 
    def __init__(self, content, done):
        self.content = content
        self.done = False
        self.created_at = datetime.utcnow()
 
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
            todo = Todo(request.form['content'])
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('new.html') 
 
if __name__ == '__main__':
    app.run()