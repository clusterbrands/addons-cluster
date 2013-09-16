from openerp.addons.web import controllers


class Session(controllers.main.Session):

    def session_info(self, req):

        req.session.ensure_valid()
        context = req.session.get_context() if req.session._uid else {}
        context.update({'remote_addr': req.httprequest.environ['REMOTE_ADDR']})
        return {
            "session_id": req.session_id,
            "uid": req.session._uid,
            "user_context": context,
            "db": req.session._db,
            "username": req.session._login,
        }
