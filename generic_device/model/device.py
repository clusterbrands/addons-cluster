from openerp.osv.orm import except_orm
from openerp.osv import osv, fields
from openerp.tools.translate import _


class generic_device(osv.Model):

    _name = "generic.device"

    def _print_error(self, error, msg):
        '''
        shows an error on the screen
        '''
        raise osv.except_osv(error, msg)

    def _get_config(self, cr, uid, context=None):
        self._print_error("Implementation error",
                          _("The method _get_config() must be overriden"))

    def _get_cpath(self, cr, uid, context=None):
        self._print_error("Implementation error",
                          _("The method _get_cpath() must be overriden"))

    def _make_command(self, cr, uid, command, params, config=True,
                      context=None):
        context = context or {}
        cfg = {}
        url = "http://localhost:8069" + /
            self._get_cpath(cr, uid, context=context)
        if (config):
            cfg = self._get_config(cr, uid, context=context)
        req_params = {
            'command': command, 'params': params, 'config': cfg
        }
        req_params_str = urllib.urlencode(req_params)
        request = urllib2.Request(url, req_params_str)
        return request

    def send_command(self, cr, uid, command, params={}, config=True,
                     context=None):
        context = context or {}
        response = {}
        request = self._make_command(cr, uid, name, params, config,
                                     context=context)
        try:
            response = urllib2.urlopen(request)
        except HTTPError as e:
            self._print_error("HTTP ERROR !",
                              e.reason.decode('utf-8'))
        except URLError as e:
            self._print_error("URL ERROR !",
                              e.reason.strerror.decode('utf-8'))

        response = json.loads(response.read())
        if response['status'] == 'error':
            self._print_error("COMMAND ERROR", response['error'])
        return response['values']
