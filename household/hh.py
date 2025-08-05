from flask import *
from db.db import brgy_list,connection,hh_list,hh_member,list
from map.map import individual_mark
import folium
from functions.functions import pdf

hh=Blueprint('hh',__name__,template_folder='../templates/household',url_prefix='/Household')


@hh.route('/')
def home():
    return render_template('household.html')
@hh.route('/new',methods=['get','post'])
def new():
    brgy=brgy_list()
    hh=hh_list()
    if request.method=='POST':
        try:
            db=connection()
            cur=db.cursor()
            hh=request.form['hh']
            province=request.form['province']
            municipality=request.form['municipality']
            barangay=request.form['barangay']
            address=request.form['address']
            latitude=request.form['latitude']
            longitude=request.form['longitude']
            cur.execute("""Insert into household_information(number,province,municipality,barangay,purok,lat,long)
                            values(?,?,?,?,?,?,?)""",
                            (hh,province,municipality,barangay,address,latitude,longitude))
            db.commit()
            return redirect(url_for('hh.hh_lst'))
        except Exception as e:
            return str(e)
    else:    
        brgy=brgy_list()
        hh=hh_list()
        return render_template('new.html',brgy=brgy,hh=hh)
    
@hh.route('/individual_marking/<hh>')
def hh_mark(hh):
    try:
        db=connection()
        cur=db.cursor()
        cur.execute("Select number,lat,long from household_information where number='"+hh+"'")
        rw=cur.fetchall()
        l=[rw[0][1],rw[0][2]]
        mp=folium.Map(location=l,zoom_start=18)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satelite",
            overlay=True,
            control=True,).add_to(mp)
        individual_mark(hh,mp,l)
        mp.save('./templates/map.html')
        return render_template('map.html')
    except Exception as e:
         return "<br><br><p style='text-align:center'> Something Error in Finding Location <br> "+str(e)+"</p>"

@hh.route('/hh_list_all')
def hh_lst():
            hh=hh_list()
            html= render_template('rbiforma.html',rw=hh)
            return pdf(html,'folio','landscape').report()

#household member

@hh.route('/hh_member_new/<h>')
def hh_member_new(h):
            hh=hh_member(h)
            l=list(hh).relation()
            m=list(hh).marital_status()
            r=list(hh).religion()
            e=list(hh).ethnic()
            v=list(h).voters()
            hl=list(h).household_members()
            o=list(h).occupation()
            return render_template('new_member.html',hh=hh,h=h,l=l,m=m,r=r,e=e,v=v,hl=hl,o=o)
@hh.route('/hh_member_delete/<key>/<hh>')
def hh_member_delete(key,hh):
      db=connection()
      cur=db.cursor()
      cur.execute("Delete from inhabitants where id='"+key+"'")
      db.commit()
      return redirect(url_for('hh.hh_member_new',h=hh))

@hh.route('/demographic_entry',methods=['get','post'])
def demographic_entry():
      if request.method=='POST':
            return jsonify({'idno':12425,'msg':'Demographic Data Successfully Save!'})
      else:
            return jsonify({'idno':'sdf','msg':'Demographic Data Successfully Save!'})
            