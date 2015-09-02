from openerp.addons.web import controllers
from openerp import http
from openerp.http import request

class Session(controllers.main.Session):

    def session_info(self):

        request.session.ensure_valid()
        context = request.session.get_context() if request.session._uid else {}
        context.update({'remote_addr': request.httprequest.environ['REMOTE_ADDR']})
        return {
            "session_id": request.session_id,
            "uid": request.session._uid,
            "user_context": context,
            "db": request.session._db,
            "username": request.session._login,
        }
