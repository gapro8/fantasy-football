import bottle
import model
from bottle import *




@get('/')
def index():
    moji_igralci, ime_ekipe = model.moji_igralci(), model.ime_moje_ekipe()
    return template("moja_ekipa.html", moji_igralci=moji_igralci, ime_ekipe=ime_ekipe)

@get('/pregled_baze')
def pregled_baze():
    Country, League, Match, Player, Player_Attributes, Team, Team_Attributes = model.pregled()
    return template("pregled_tabel.html", Country=Country, League=League, Match=Match, Player=Player, Player_Attributes=Player_Attributes, Team=Team, Team_Attributes=Team_Attributes)


####################################################################################
# quick match
####################################################################################

@get('/quick_match')
def load_quick_match():
    # TODO naj to bere iz drop down menija ali pa da pises ime ekipe in ti ponuja izbira (se bom se odlocil)
    home_team = 10194 # request.forms.get('home_team')
    away_team = 10260 # request.forms.get('away_team')
    return template("quick_match.html", home_igralci=[], away_igralci=[], poz=model.POZICIJE)


@post('/quick_match')
def load_quick_match():
    # TODO naj to bere iz drop down menija ali pa da pises ime ekipe in ti ponuja izbira (se bom se odlocil)
    # TODO pogruntaj zakaj select ne vrne igralcev za mojo ekipo
    home_team = request.forms.get('home_team')
    away_team = request.forms.get('away_team')

    home_igralci, away_igralci = model.igralci_v_ekipi(home_team), model.igralci_v_ekipi(away_team)

    return template("quick_match.html", home_igralci=home_igralci, away_igralci=away_igralci, poz=model.POZICIJE)

# TODO naredi tako da lahko izberes igralce in dodaj gumb odigraj tekmo

@post('/simuliraj_tekmo')
def simuliraj_tekmo():
    # grdo ampak deluje
    max_stevilo_igralcev_izmed_vseh_ekip = 30
    seznam_home_igralcev = []
    seznam_away_igralcev = []
    for i in range(max_stevilo_igralcev_izmed_vseh_ekip):
        id_home = request.forms.get(str(i))
        if id_home != None: seznam_home_igralcev.append(id_home)
        id_away = request.forms.get(str(i+max_stevilo_igralcev_izmed_vseh_ekip))
        if id_away != None: seznam_away_igralcev.append(id_away)

    if len(seznam_home_igralcev) != 11: return "V domači ekipi ni 11 igralcev"
    if len(seznam_away_igralcev) != 11: return "V gostojoči ekipi ni 11 igralcev"

    res = model.f_izracunaj_stohasticen_rezultat(seznam_home_igralcev, seznam_away_igralcev)
    return res



####################################################################################
# lestvica
####################################################################################

@get('/lestvica')
def izberi_lestico():
    return template("liga.html", lestvica=[])

@post('/lestvica')
def do_lestvica():
    league_id = request.forms.get('liga')
    sezona = request.forms.get('sezona')
    krog = int(request.forms.get('krog'))
    lest_sortirana = model.naredi_lestvico(league_id, sezona, krog)
    return template("liga.html", lestvica=lest_sortirana)




####################################################################################
# transfer market
####################################################################################

@get('/naredi_ekipo')
def naredi_ekipo():
    moji_igralci = model.moji_igralci()
    return template("izbor_igralcev.html", moji_igralci=moji_igralci, igralci=[], poz=model.POZICIJE, f_cena=model.f_cena, url=bottle.url)


@post('/naredi_ekipo')
def sestavi_ekipo():
    ime_igralca = request.forms.get('igralec')
    vratar = request.forms.get('vratar')
    branilec = request.forms.get('branilec')
    vezist = request.forms.get('vezist')
    napadalec = request.forms.get('napadalec')
    sez_igralcev = model.seznam_igralcev_za_prikaz(ime_igralca, vratar, branilec, vezist, napadalec)
    return template("izbor_igralcev.html", moji_igralci=[], igralci = sez_igralcev, poz=model.POZICIJE, f_cena=model.f_cena, url=bottle.url)

@post('/kupi/<igralec_id>')
def kupi(igralec_id):
    model.kupi(igralec_id)
    return redirect(url('/naredi_ekipo'))

# TODO podobno kot kupi (rabil bom player_api_id), tako kot je narejeno v izbor_igralcev.html 56 vrstica
@post('/prodaj/<igralec_id>')
def prodaj(igralec_id):
    model.prodaj(igralec_id)
    return redirect(url('/naredi_ekipo'))



#da izpiše vse igralce
@get('/ekipa/<ime_ekipe>')
def ekipa(ime_ekipe):
    ime_ekipe, igralci = model.ekipa_model(ime_ekipe)
    return template("ekipa.html", ime_ekipe=ime_ekipe, igralci=igralci)




# @get('/lestvica/<league_id>')
# def lestvica(league_id):
#     s = f"SELECT Team.team_long_name, Team.team_short_name FROM Team JOIN League ON Team.league_id = League.id where League.id = {league_id}"
#     res = cur.execute(s)
#     teams = res.fetchall()
#     print(teams)
#     return template("lestvica.html", ekipe=teams)


# @get('/lestvica/<league_id>')
# def lestvica(league_id):
#     s = f"SELECT Team.team_long_name, Team.team_short_name FROM Team JOIN League ON Team.league_id = League.id where League.id = {league_id}"
#     res = cur.execute(s)
#     teams = res.fetchall()
#     print(teams)
#     return template("lestvica.html", ekipe=teams)

# @get('/uredi_ekipo')
# def uredi_ekipo():
#     cur.execute("SELECT * FROM Player;")
#     Player = cur.fetchall()
#     return template("igralci.html", Player = Player)


# @get('/igralec/<ime_igralca>')
# def igralec(ime_igralca):
#     s = f'''SELECT Player.birthday, Team.team_long_name, Team.team_short_name, 
#             Player.player_coordinate_x, Player.player_coordinate_y FROM Player 
#             JOIN Team ON Player.team_id = Team.team_api_id
#             WHERE Player.player_name = {ime_igralca}'''
#     res = cur.execute(s)
#     atributi = res.fetchall()
#     return template("igralec.html",ime_igralca = ime_igralca)


# @post('/lestvica')
# def do_lestvica():
#     league_id = request.forms.get('liga')
#     sezona = request.forms.get('sezona')
#     print(league_id, sezona)
#     s = f"SELECT Team.team_long_name, Team.team_short_name FROM Team JOIN League ON Team.league_id = League.id where League.id = {league_id}"
#     res = cur.execute(s)
#     teams = res.fetchall()
#     print(teams)
#     return template("lestvica.html", ekipe=teams)


bottle.run(debug=True, reloader=True)