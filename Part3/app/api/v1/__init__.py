from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns

api = Api(
    title='HBnB API',
    version='1.0',
    description='HBnB REST API'
)

api.add_namespace(users_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')
