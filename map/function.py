from flask import *
import folium
from folium.features import DivIcon
import sqlite3
from db.db import connection



def plot_marked():
    map=folium.Map(location=[6.53382, 124.56370],zoom_start=10)
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    ).add_to(map)
    db=sqlite3.connect('./db/data.db')
    cur=db.cursor()
    cur.execute("Select number,lat,long from household_information where lat not null")
    rw=cur.fetchall()
    a=[]
    for i in rw:
        if i[1]!='' or i[2]!='':
            l=[i[1],i[2]]
            folium.Marker(location=l,tooltip='<a>'+i[0]+'</a>',icon_color='green').add_to(map)
            a.append(l)   
    map.save('./templates/map.html')


def brgy_area(brgy):
    db=connection()
    cur=db.cursor()
    rw=cur.execute("SELECT * from area INNER join barangay on barangay.id=BRGY where brgy='"+ str(brgy) + "'").fetchall()
    map=folium.Map(location=[6.53382, 124.56370],zoom_start=10)
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    ).add_to(map)
    b=[]
    for i in rw:
        b.append([i[1],i[2]])

    folium.Polygon(locations=b,popup=rw[6]).add_to(map)
    map.save('./templates/map.html')


    



