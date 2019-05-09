from flask_restplus import reqparse

pdf_arg = reqparse.RequestParser()
pdf_arg.add_argument('text', type=str, help='input text', default='أهلا بك في عالم بايثون!')
