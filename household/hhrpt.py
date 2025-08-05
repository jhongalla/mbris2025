from flask import *
from db.db import connection




hhrpt=Blueprint('hhrpt',__name__,template_folder='../templates/household',url_prefix='/hh_reports')

@hhrpt.route('/rbiforma')
def rbiforma():
    db=connection()
    cur=db.cursor()
    cur.execute("Select * from inhabitants")
    rw=cur.fetchall()
    return render_template('rbiforma.html',rw=rw)

@hhrpt.route('/rbiformb')
def rbiformb():
    db=connection()
    cur=db.cursor()
    cur.execute("Select * from inhabitants")
    rw=cur.fetchall()
    return render_template('rbiformb.html',rw=rw)