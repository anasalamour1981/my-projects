import xlsxwriter
import base64

from openerp import http, exceptions
from openerp.http import request



class ExcelController(http.Controller):

    @http.route('/web/base_odex/export', type='http', auth='user')
    def report(self, token, workbook=None, **kw):
        if not workbook:
            raise exceptions.Warning(('No Workbook selected to download!'))
        workbook = base64.decodestring(workbook)
        response = request.make_response(
            workbook,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', 'attachment; filename=' + 'abc' + '.xls;')
            ]
        )
        response.set_cookie('fileToken', token)
        return response
