import logging
from io import BytesIO

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from flask import request, send_file
from flask_restplus import Resource

from api.restplus import utils
from api.endpoints.parsers import pdf_arg

log = logging.getLogger(__name__)

ns = utils.namespace('pdf', description='Arabic PDF generator')

PAGE_SIZE = (600, 200)
FONT_SIZE = 22
RGB_COLOR = (0, 0, 0)


def write_pdf(input_text):
    pdfmetrics.registerFont(TTFont('JannaBold', 'resources/Bahij_Janna-Bold.ttf'))
    packet = BytesIO()
    canv = canvas.Canvas(packet)
    canv.setPageSize(PAGE_SIZE)
    canv.setFillColorRGB(*RGB_COLOR)
    canv.setFont('JannaBold', FONT_SIZE)
    canv.drawImage('resources/Python-Logo.png', 0, 0, mask='auto')
    canv.drawRightString(PAGE_SIZE[0] - 10, 10, get_display(arabic_reshaper.reshape(input_text)))
    canv.save()
    packet.seek(0)
    return packet


@ns.route('/generate')
class PDFGenerator(Resource):
    """ generate PDF file """
    @ns.response(200, 'Success')
    @ns.response(400, 'Error')
    @ns.doc(parser=pdf_arg)
    @ns.expect(pdf_arg)
    def get(self):
        """
        generate PDF file
        """
        args = pdf_arg.parse_args(request)
        input_text = args.get('text')
        output_file = write_pdf(input_text)

        return send_file(output_file, as_attachment=True, attachment_filename='example.pdf',
                         mimetype='application/pdf')
