from flask import Flask,render_template,url_for,redirect
from db.db import connection,brgy_list
from household.hh import hh
import folium
from map.map import main_map,layer_gmap
from household.hhrpt import hhrpt




app=Flask(__name__)
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.register_blueprint(hh)
app.register_blueprint(hhrpt)
@app.route('/')
def home():
    db=connection()
    cur=db.cursor()
    rw=cur.execute('select * from religion').fetchall()
    return render_template('index.html',rw=rw)
@app.route('/map')
def map():
    mp=folium.Map(location=[6.53382, 124.56370],zoom_start=10,world_copy_jump=False)
    layer_gmap(mp)
    db=connection()
    cur=db.cursor()
    cur.execute("select popcomno,HOUSEHOLD_INFORMATION.LAT,HOUSEHOLD_INFORMATION.long from inhabitants INNER join HOUSEHOLD_INFORMATION on inhabitants.popcomno=HOUSEHOLD_INFORMATION.NUMBER")
    rw=cur.fetchall()
    for i in rw:
        try:
            l=[i[1],i[2]]
            folium.Marker(location=l).add_to(mp)
        except:
            pass
    D=brgy_list()
    try:
        for i in D:
            main_map(i[0],mp,i[2]).brgy_polygon()

        mp.save('./templates/map.html')
        return render_template('map.html')
    except Exception as e:
        return str(e)
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port='3000')