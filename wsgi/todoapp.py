from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
 
    def __init__(self, content):
        self.content = content
        self.done = False
        self.created_at = datetime.utcnow()
 
@app.route('/')
def index():
    return render_template('index.html',
        todos=Todo.query.order_by(Todo.created_at.desc()).all()
    )

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
            todo = Todo(request.form['content'])
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
    return render_template('new.html')

@app.route('/todos/<int:todo_id>', methods = ['GET' , 'POST'])
def show_or_update(todo_id):
    todo_item = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template('view.html',todo=todo_item)
    todo_item.content = request.form['content']
    todo_item.done  = ('done.%d' % todo_id) in request.form
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run()