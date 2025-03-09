from flask_restful import Resource

class HelloWorld(Resource):

    def get(self):
        return ({"message":"Welcome to your Flask App"},200)