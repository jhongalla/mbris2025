from flask import * 
from folium.features import *
import folium as f
from db.db import connection


class main_map:
    def __init__(self,b=None,m=None,c=None):
        self.brgy=b
        self.mp=m
        self.color=c
    def brgy_polygon(self):
        try:
            db=connection()
            cur=db.cursor()
            rw=cur.execute("SELECT * from area INNER join barangay on barangay.id=BRGY where brgy='"+ str(self.brgy) + "'").fetchall()
            b=[]
            for i in rw:
                b.append([i[1],i[2]])
            f.Polygon(locations=b,popup=rw[0][5],color=self.color,fill_color=self.color,fill_opacity=.2).add_to(self.mp)
        except:
            db.rollback()
    def hh_mark(self):
            try:
                db=connection()
                cur=db.cursor()
                cur.execute("Select number,lat,long from household_information where lat not null")
                rw=cur.fetchall()
                a=[]
                for i in rw:
                    if i[1]!='' or i[2]!='':
                        l=[float(i[1]),float(i[2])]
                        f.Marker(location=l,tooltip='<a>'+i[0]+'</a>',icon=Icon(color=self.color),color='black').add_to(self.mp)
                        a.append(l) 
                    else:
                         return f'Something Error'
            except Exception as e:
                 return str(e)
    def coor(self):
        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' ° ';};"
        f.plugins.MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(self.m)  

def individual_mark(hh,map,l):
            a="""<div style='background-color:black;
                            width:300px;padding:10px;color:yellow;

            
            '><p style='Width:200px'>"""+"""LOCATION : """ + str(l) +"<br> House Hold Number : "+ str(hh)+"</p>"
            ""
            "</div>"""
            try:
                f.Marker(location=l,popup=a,tooltip=l).add_to(map)
            except Exception as e:
                 return 404
def layer_gmap(mp):
            f.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satelite",
            overlay=True,
            control=True,).add_to(mp)
