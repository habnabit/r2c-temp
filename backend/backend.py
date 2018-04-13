from zope.interface import Interface, Attribute, implementer
from twisted.python.components import registerAdapter
from twisted.web.server import Session
import attr
import base64
import json
import klein
import os


class IUser(Interface):
    """A user."""
    name = Attribute("The user's name")


@implementer(IUser)
@attr.s()
class User(object):
    name = attr.ib(default=None)

    @classmethod
    def fromSession(cls, session):
        return cls()


registerAdapter(User.fromSession, Session, IUser)


@attr.s()
class Document(object):
    id = attr.ib()
    content = attr.ib()
    users = attr.ib(default=attr.Factory(set))
    owner = attr.ib(default=None)

    def asJSON(self, viewer):
        return {
            'content': self.content,
            'otherUsers': list(self.users - {viewer}),
            'youAreOwner': self.owner == viewer,
        }


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

    @app.route('/api/doc', methods=['GET'])
    def api_docs(self, request):
        return asJSON(request, self.documents.keys())

    @app.route('/api/whoami', methods=['GET'])
    def api_whoami_get(self, request):
        return asJSON(request, {'user': self.whoami(request).name})

    @app.route('/api/whoami', methods=['PUT'])
    def api_whoami_set(self, request):
        body = json.load(request.content)
        if body['user'] in self.users:
            request.setResponseCode(409)
            return asJSON(request, {})

        user = self.whoami(request)
        user.name = body['user']
        self.users[user.name] = user
        return asJSON(request, {'user': user.name})

    @app.route('/api/doc', methods=['POST'])
    def api_doc_create(self, request):
        body = json.load(request.content)
        doc = Document(content=body['content'], 
                       id=base64.b64encode(os.urandom(9)))
        self.documents[doc.id] = doc
        return asJSON(request, {'created': True, 'id': doc.id})

    @app.route('/api/doc/<docId>')
    def api_docs(self, request, docId):
        doc = self.documents.get(docId)
        if doc is None:
            request.setResponseCode(404)
            return asJSON(request, {})
        else:
            user = self.whoami(request)
            if doc.owner is None:
                doc.owner = user
            doc.users.add(user)
            return asJSON(request, doc.asJSON(user))


DocStore().app.run('localhost', 7070)
