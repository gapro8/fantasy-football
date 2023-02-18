import bottle
from bottle import get, post, template
import sqlite3


@get('/')
def index():
    name = "John"
    return bottle.template("index.html", name=name)


@get('/pregled_baze')
def pregled_baze():
    cur.execute("SELECT * FROM Country limit 10;")
    Country = cur.fetchall()
    cur.execute("SELECT * FROM League limit 10;")
    League = cur.fetchall()
    cur.execute("SELECT * FROM Match limit 10;")
    Match = cur.fetchall()
    cur.execute("SELECT * FROM Player limit 10;")
    Player = cur.fetchall()
    cur.execute("SELECT * FROM Player_Attributes limit 10;")
    Player_Attributes = cur.fetchall()
    cur.execute("SELECT * FROM Team limit 10;")
    Team = cur.fetchall()
    cur.execute("SELECT * FROM Team_Attributes limit 10;")
    Team_Attributes = cur.fetchall()
    return bottle.template("pregled_tabel.html", Country=Country, League=League, Match=Match, Player=Player, Player_Attributes=Player_Attributes, Team=Team, Team_Attributes=Team_Attributes)


baza = "baza_nogomet.db"
con = sqlite3.connect(baza)
cur = con.cursor()


bottle.run(debug=True, reloader=True)