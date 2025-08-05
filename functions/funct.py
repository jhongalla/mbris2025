import sqlite3

def check_voters(id):
    db=sqlite3.connect('./db/data.db')
    cur=db.cursor()
    cur.execute("select * from inhabitants where id='"+id+"'")
    rw=cur.fetchall()
    res=''
    for i in rw:
            p=f'{i[1]}, {i[2]} {i[3]}'
            try:
                cur.execute("select * from voters where fullname like'%"+p+"%'")
                v=cur.fetchall() 
                res=v[0]
            except:
                db.rollback()
    return res
