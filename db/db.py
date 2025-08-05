import sqlite3

def connection():
    db=sqlite3.connect('./db/data.db')
    return db

def brgy_list():
        db=connection()
        cur=db.cursor()
        cur.execute("select * from barangay")
        rw=cur.fetchall()
        return rw

def hh_list():
        db=connection()
        cur=db.cursor()
        cur.execute("""SELECT *,CASE
                        WHEN STRFTIME('%m', 'now') > STRFTIME('%m', birthdate) THEN
                              STRFTIME('%Y', 'now') - STRFTIME('%Y', birthdate)
                        WHEN STRFTIME('%m', 'now') = STRFTIME('%m', birthdate) AND STRFTIME('%d', 'now') >= STRFTIME('%d', birthdate) THEN
                              STRFTIME('%Y', 'now') - STRFTIME('%Y', birthdate)
                        ELSE
                              STRFTIME('%Y', 'now') - STRFTIME('%Y', birthdate) - 1
                        END AS age from inhabitants INNER join HOUSEHOLD_INFORMATION on HOUSEHOLD_INFORMATION.NUMBER=inhabitants.popcomno
                        """)
        rw=cur.fetchall()
        return rw

def hh_member(q):
        db=connection()
        cur=db.cursor()
        cur.execute("select * from inhabitants where popcomno='"+q+"'")
        rw=cur.fetchall()
        return rw

class list:
        def __init__(self,c=None):
              self.c=c
              sdb=sqlite3.connect('./db/data.db')
              self.sdb=sdb
              self.cur=sdb.cursor()
        def relation(self):
              rw=self.cur.execute("select * from RELATION_TO_HOUSEHOLD").fetchall()
              return rw
        
        def occupation(self):
              rw=self.cur.execute("select * from occupations").fetchall()
              return rw
        def marital_status(self):
              rw=self.cur.execute("select * from marital").fetchall()
              return rw
        def religion(self):
              rw=self.cur.execute("select * from religion").fetchall()
              return rw
        def ethnic(self):
              rw=self.cur.execute("select * from ethnic").fetchall()
              return rw
        def voters(self):
                  self.cur.execute("select * from inhabitants where popcomno='"+ self.c +"'")
                  rw=self.cur.fetchall()
                  b=[]
                  for i in rw:
                              try:
                                    self.cur.execute("select * from voters where fullname like'%"+f'{i[1]}, {i[2]} {i[3]}'+"%' or fullname like'%"+f'{i[1]}, {i[2]} {i[4]}'+"%' order by fullname")
                                    v=self.cur.fetchall() 
                                    for j in v:
                                           b.append(j)
                              except:
                                     self.sdb.rollback()
                  return b
                              
        def household_members(self):
                  self.cur.execute("select inhabitants.id,popcomno,lname,fname,mname,nameext,sex,birthdate,RELATION_TO_HOUSEHOLD.DESCRIPTION  from inhabitants INNER join RELATION_TO_HOUSEHOLD on RELATION_TO_HOUSEHOLD.ID=relationship where popcomno='"+ self.c +"'")
                  rw=self.cur.fetchall()
                  return rw
              
              
              
        
        