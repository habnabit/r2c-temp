from zope.interface import Interface, Attribute, implementer
from twisted.python.components import registerAdapter
from twisted.web.server import Session
import attr
import json
import klein


class IUser(Interface):
    """A user."""
    name = Attribute("The user's name")


@implementer(IUser)
@attr.s()
class User(object):
    name = attr.ib(default=None)

    @classmethod
    def from_session(cls, session):
        return cls()


registerAdapter(User.from_session, Session, IUser)


def asJSON(request, obj):
    request.setHeader('Content-Type', 'application/json')
    return json.dumps(obj)


@attr.s(cmp=False)
class DocStore(object):
    documents = attr.ib(default=attr.Factory(dict))
    users = attr.ib(default=attr.Factory(dict))

    def whoami(self, request):
        return IUser(request.getSession())

    app = klein.Klein()

    @app.route('/api/doc')
    def api_docs(self, request):
        return asJSON(request, self.documents.keys())

    @app.route('/api/whoami', methods=['GET'])
    def api_whoami_get(self, request):
        return asJSON(request, {'user': self.whoami(request).name})

    @app.route('/api/whoami', methods=['PUT'])
    def api_whoami_set(self, request):
        content = json.load(request.content)
        if content['user'] in self.users:
            request.setResponseCode(409)
            return asJSON(request, {})

        user = self.whoami(request)
        user.name = content['user']
        self.users[user.name] = user
        return asJSON(request, {'user': user.name})


DocStore().app.run('localhost', 7070)
