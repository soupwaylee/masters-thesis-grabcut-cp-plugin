from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.routing import Rule
import sys
import os
import logging

app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Plugin grabcut API',
    description='A simple TodoMVC API',
)

### Database ###
db = SQLAlchemy(app)

from models import TodoModel

# Needed to initialize/migrate the database
# https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate(app, db) 

### API ###

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})

class TodoDAO(object): # DAO = Data Access Object
    def __init__(self, session):
        self.session = session

    def todos(self):
        return self.session.query(TodoModel).all()

    def get(self, id):
        if todo:=self.session.query(TodoModel).get(id):
            return todo
        else:
            api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        app.logger.debug(f"Creating ToDo: {str(data)}")
        todo = TodoModel(task=data["task"])
        self.session.add( todo )
        self.session.commit()
        return todo

    def update(self, id, data):
        todo = self.session.query(TodoModel).get(id)
        todo.task = data["task"]
        self.session.commit()
        return todo

    def delete(self, id):
        self.session.delete(TodoModel.query.get(id))
        self.session.commit()


DAO = TodoDAO(db.session)

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos()

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    # THIS IS NOT BEING EXECUTED
    # To cater for the URL prefix when running with "cellphaser start",
    # "gunicorn" is used to serve this app (see ../Dockerfile)
    app.run(debug=True, host='0.0.0.0')