import random
import sqlite3


baza = "baza_nogomet.db"
con = sqlite3.connect(baza)
cur = con.cursor()

POZICIJE = {1:"GK", 2:"DEF", 3:"DEF", 4:"DEF", 5:"DEF", 6:"MID", 7:"MID", 8:"MID", 9:"ATK", 10:"ATK", 11:"ATK"}


def pregled():
    cur.execute("SELECT * FROM Country limit 10;")
    Country = cur.fetchall()
    cur.execute("SELECT * FROM League limit 10;")
    League = cur.fetchall()
    cur.execute("SELECT * FROM Match limit 10;")
    Match = cur.fetchall()
    # cur.execute("SELECT player_api_id, player_name, player_fifa_api_id, birthday, team_id, player_coordinate_x, player_coordinate_y FROM Player WHERE player_name in ('Lionel Messi')")
    cur.execute("SELECT * FROM Player order by id desc limit 10;")
    #cur.execute("SELECT count(*) FROM Player where team_id not null;")
    Player = cur.fetchall()
    cur.execute("SELECT * FROM Player_Attributes limit 10;")
    Player_Attributes = cur.fetchall()
    cur.execute("SELECT * FROM Team limit 10;")
    Team = cur.fetchall()
    cur.execute("SELECT * FROM Team_Attributes limit 10;")
    Team_Attributes = cur.fetchall()
    return Country, League, Match, Player, Player_Attributes, Team, Team_Attributes

def moji_igralci():
    # TODO namesto * napisem ustrezne stolpce
    # TODO ta select ne dela
    s = f"""SELECT Player.player_api_id, Player.player_name, Player.birthday, Team.team_long_name, Team.team_short_name, Player.player_coordinate_x, Player.player_coordinate_y, Player_Attributes.overall_rating FROM Player 
            JOIN Team ON Player.team_id = Team.team_api_id 
            JOIN Player_Attributes ON Player.player_api_id = Player_Attributes.player_api_id
            WHERE Player.team_id = 50000
            ORDER BY Player_Attributes.overall_rating DESC;
    """
    cur.execute(s)
    moji_igralci = cur.fetchall()
    return moji_igralci

def ime_moje_ekipe():
    s = "SELECT team_long_name FROM Team WHERE team_api_id = 50000;"
    cur.execute(s)
    ime_ekipe = cur.fetchone()
    return ime_ekipe


def naredi_lestvico(league_id, sezona, krog):
    slovar_lest = izracunaj_lestvico(league_id, sezona, krog)
    lest = [(ekipa_id, Z, R, P, dani_goli, prejeti_goli) for  ekipa_id, (Z, R, P, dani_goli, prejeti_goli) in slovar_lest.items()]
    #lest.sort()
    lest_sortirana = sorted(lest, key=prvi_na_vrsti, reverse=True)   #sortiramo po tockah (prvi bo na prvem mestu)
    # reverse=True poskrbi da gre od najvecjega stevila tock do najmanjsega
    return lest_sortirana

# Spodnjo funkcijo uporabimo v def do_lestvica() zgoraj, da izracunamo stevilo tock in gol razliko. Po temu potem sortiramo lestvico. Najprej tocke potem gol razlika.
def prvi_na_vrsti(elem):
    return (elem[1] * 3 + elem[2], elem[4] - elem[5])  #uporabimo tuple

def izracunaj_lestvico(league_id, season, krog=100):
    tekme = vse_tekme_v_sezoni(league_id, season, krog) 
    sl = {} # {ekipa_id: (Z, R, P, dani_goli, prejeti_goli)}
    for stage, date, home_team_id, away_team_id, home_team_goals, away_team_goals in tekme:
        if home_team_id not in sl:
            if home_team_goals > away_team_goals: 
                sl[home_team_id] = (1, 0, 0, home_team_goals, away_team_goals)
            elif home_team_goals < away_team_goals:
                sl[home_team_id] = (0, 0, 1, home_team_goals, away_team_goals)
            elif home_team_goals == away_team_goals:
                sl[home_team_id] = (0, 1, 0, home_team_goals, away_team_goals)
        else:
            Z, R, P, dani_goli, prejeti_goli = sl[home_team_id]
            dani_goli += home_team_goals
            prejeti_goli += away_team_goals
            if home_team_goals > away_team_goals: Z += 1
            elif home_team_goals < away_team_goals: P += 1
            elif home_team_goals == away_team_goals: R += 1
            sl[home_team_id] = (Z, R, P, dani_goli, prejeti_goli)

        if away_team_id not in sl:
            if away_team_goals > home_team_goals:
                sl[away_team_id] = (1, 0, 0, away_team_goals, home_team_goals)
            elif away_team_goals < home_team_goals:
                sl[away_team_id] = (0, 0, 1, away_team_goals, home_team_goals)
            elif away_team_goals == home_team_goals:
                sl[away_team_id] = (0, 1, 0, away_team_goals, home_team_goals)
        else:
            Z, R, P, dani_goli, prejeti_goli = sl[away_team_id]
            dani_goli += away_team_goals
            prejeti_goli += home_team_goals
            if away_team_goals > home_team_goals: Z += 1
            elif away_team_goals < home_team_goals: P += 1
            elif away_team_goals == home_team_goals: R += 1    
            sl[away_team_id] = (Z, R, P, dani_goli, prejeti_goli)        
    return sl


def vse_tekme_v_sezoni(league_id, season, stage=100):
    s2 = f"""
    SELECT 
        stage, date, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal
        FROM Match
        WHERE league_id = {league_id} AND season = '{season}' AND stage <= {stage}
        ORDER BY league_id, stage;
    """
    res = cur.execute(s2)
    tekme = res.fetchall()
    return tekme

def igralci_v_ekipi(team):
    # TODO pogruntaj zakaj select ne vrne igralcev za mojo ekipo
    s = f"""SELECT Player.player_api_id, Player.player_name, Player.birthday, Team.team_long_name, Team.team_short_name, Player.player_coordinate_x, Player.player_coordinate_y, Player_Attributes.overall_rating FROM Player 
    JOIN Team ON Player.team_id = Team.team_api_id 
    JOIN Player_Attributes ON Player.player_api_id = Player_Attributes.player_api_id
    WHERE Player.team_id = {team}
    ORDER BY Player_Attributes.overall_rating DESC;"""
    cur.execute(s) 
    res = cur.fetchall()
    return res

def ekipa_model(ime_ekipe):
    s = f"""SELECT Player.player_name, Player.birthday, Team.team_long_name, Team.team_short_name, Player.player_coordinate_x, Player.player_coordinate_y FROM Player 
            JOIN Team ON Player.team_id = Team.team_api_id WHERE Team.team_long_name = '{ime_ekipe}';"""
    res = cur.execute(s) 
    igralci = res.fetchall()
    return ime_ekipe, igralci

def seznam_igralcev_za_prikaz(ime_igralca, vratar, branilec, vezist, napadalec):
    polozaji = []
    if vratar != None:
        polozaji += [1]
    if branilec != None:
        polozaji += [2,3,4,5]
    if vezist != None:
        polozaji += [6,7,8]
    if napadalec != None:
        polozaji += [9,10,11]
    if len(polozaji) == 1:
        polozaji = f"({polozaji[0]})"
    else:
        polozaji = tuple(polozaji)

    s = f"""SELECT Player.player_api_id, Player.player_name, Player.birthday, Team.team_long_name, Team.team_short_name, Player.player_coordinate_x, Player.player_coordinate_y, Player_Attributes.overall_rating FROM Player 
    JOIN Team ON Player.team_id = Team.team_api_id 
    JOIN Player_Attributes ON Player.player_api_id = Player_Attributes.player_api_id
    WHERE Player.player_coordinate_y in {polozaji} AND Player.player_name like '%{ime_igralca}%' 
    ORDER BY Player_Attributes.overall_rating DESC;"""
    res = cur.execute(s) 
    sez_igralcev = res.fetchall()
    return sez_igralcev


def f_cena(r):
    r = int(r) if r != None else 1
    if r > 70:
        return r * 100000
    else:
        return r * 1000


def f_izracunaj_stohasticen_rezultat(seznam_home_igralcev, seznam_away_igralcev):
    s_home = f"""
        SELECT overall_rating from Player_Attributes 
        WHERE player_api_id in {tuple(seznam_home_igralcev)}
    """
    cur.execute(s_home)
    vsi = cur.fetchall()
    home_rating = sum(x[0] for x in vsi)
    s_away = f"""
        SELECT overall_rating from Player_Attributes 
        WHERE player_api_id in {tuple(seznam_away_igralcev)}
    """
    cur.execute(s_away)
    vsi = cur.fetchall()
    away_rating = sum(x[0] for x in vsi)
    print(home_rating, away_rating)
    smiselni_rezultati = ["0 : 0", "0 : 1", "0 : 2", "0 : 3", "1 : 0", "1 : 1", "1 : 2", "1 : 3", "2 : 0", "2 : 1", "2 : 2", "2 : 3", "3 : 0", "3 : 1", "3 : 2", "3 : 3"] 
    return random.choice(smiselni_rezultati) + f" home rating:{home_rating}, away rating:{away_rating}"

def kupi(igralec_id):
    cur.execute(f"SELECT player_api_id, player_name, player_fifa_api_id, birthday, team_id, player_coordinate_x, player_coordinate_y FROM Player WHERE player_api_id = {igralec_id};")
    player_api_id, player_name, player_fifa_api_id, birthday, team_id, player_coordinate_x, player_coordinate_y = tuple(cur.fetchone())
    # TODO preveri ce je ta igralec ze med kupljenimi
    # TODO denar se mora odsteti od budgeta
    s = f"""
        INSERT INTO Player
        (player_api_id, player_name, player_fifa_api_id, birthday, team_id, player_coordinate_x, player_coordinate_y) 
        VALUES ({player_api_id}, '{player_name}', (SELECT MAX(player_fifa_api_id)+1 FROM Player), '{birthday}', 50000, {player_coordinate_x}, {player_coordinate_y});
    """ 
    cur.execute(s)
    con.commit()

def prodaj(igralec_id):
    # TODO preveri ce je ta igralec ze med kupljenimi, ce ni ga ne mores prodati!!!
    # TODO denar se mora odsteti od budgeta
    s = f"DELETE FROM Player WHERE player_api_id = {igralec_id};" 
    cur.execute(s)
    con.commit()
