import logging
from io import BytesIO

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import Table, TableStyle, Paragraph

from flask import request, send_file
from flask_restx import Resource

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

    style = ParagraphStyle(name='Normal', fontName='JannaBold', fontSize=12, leading=12. * 1.2, wordWrap='RTL')
    style.alignment = TA_RIGHT
    data = ['نص عربي', input_text]
    data = [[Paragraph(get_display(arabic_reshaper.reshape(x)), style)] for x in data]
    f = Table(data, style=TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    f.wrapOn(canv, 120, 0)
    f.drawOn(canv, 449, 150)

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
