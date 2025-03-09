from modules.util.HelloWorld import HelloWorld
from modules.api.authentication import Authentication
from modules.api.wikipedia import Wikipedea
from modules.api.tags import Tags


def init_routes(api):
    api.add_resource(HelloWorld,'/')
    api.add_resource(Authentication,'/api/auth/<string:function>')
    api.add_resource(Wikipedea,'/api/wikipedia/<string:function>')
    api.add_resource(Tags,'/api/tags/<string:function>')