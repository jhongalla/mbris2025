from datetime import date
import datetime
import pdfkit
from flask import make_response,render_template


class pdf:
        def __init__(self,html=None,size=None,orientation=None):
            self.html=html
            self.size=size
            self.orientation=orientation
            self.config=pdfkit.configuration(wkhtmltopdf='./static/wkhtmltopdf/bin/wkhtmltopdf.exe')
        def report(self):
            options = {
            'page-size': self.size,
            'orientation': self.orientation,
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'title':"GENERATED LIST",
            'footer-Font-size':'6',
                }
            pdf= pdfkit.from_string(self.html,False,configuration=self.config,options=options,verbose=True)
            response=make_response(pdf)
            response.headers['Content-Type']="application/pdf"
            response.headers['Content-Disposition']="inline;filename="+f"Generated-Report.pdf"
            return response


def calculate_age(birthdate):
  try:
    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
  except AttributeError:
    return 0
  