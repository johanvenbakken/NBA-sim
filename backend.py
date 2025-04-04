from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response, Response
import random
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()


load_dotenv()

key = os.getenv("SECRET_KEY")
fernet = Fernet(key)

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    __tablename__ = "Brukere"  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brukernavn = db.Column(db.String(50), unique=True, nullable=False)
    passord = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    dato_registrert = db.Column(db.Date, nullable=False, server_default=db.func.curdate())  # Matches `curdate()`


# Define Leaderboard model
class Leaderboard(db.Model):
    __tablename__ = "Lederbord"

    user_id = db.Column(db.Integer, db.ForeignKey("Brukere.id"), primary_key=True)
    antall_seire = db.Column(db.Integer, default=0)

class Kamper(db.Model):
    __tablename__ = "Kamper"

    kamp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spiller1 = db.Column(db.String(255), nullable=False)
    spiller2 = db.Column(db.String(255), nullable=False)
    vinner = db.Column(db.String(255), nullable=False)
    taper = db.Column(db.String(255), nullable=False)
    stilling = db.Column(db.String(255), nullable=False)
    dato = db.Column(db.DateTime, nullable=False)

app.secret_key = os.getenv("APP.SECRET_KEY")

first_request = True


@app.before_request
def clear_session_on_restart():
    global first_request
    if first_request:
        session.clear()
        first_request = False

basketball_players = {
    "PG": [
        {"name": "M Johnson", "attacking": 98, "defensive": 85},
        {"name": "S Curry", "attacking": 100, "defensive": 80},
        {"name": "C Paul", "attacking": 92, "defensive": 88},
        {"name": "R Rondo", "attacking": 85, "defensive": 75},
        {"name": "R Westbrook", "attacking": 92, "defensive": 85},
        {"name": "D Rose", "attacking": 88, "defensive": 70},
        {"name": "I Thomas", "attacking": 88, "defensive": 70},
        {"name": "A Iverson", "attacking": 91, "defensive": 70},
        {"name": "D Johnson", "attacking": 87, "defensive": 70},
        {"name": "R Miyagi", "attacking": 82, "defensive": 60}
    ],
    "SG": [
        {"name": "M Jordan", "attacking": 100, "defensive": 97},
        {"name": "K Bryant", "attacking": 98, "defensive": 93},
        {"name": "D Wade", "attacking": 92, "defensive": 85},
        {"name": "R Allen", "attacking": 93, "defensive": 60},
        {"name": "J Harden", "attacking": 95, "defensive": 65},
        {"name": "D Booker", "attacking": 93, "defensive": 75},
        {"name": "J Holiday", "attacking": 87, "defensive": 88},
        {"name": "D Mitchell", "attacking": 92, "defensive": 78},
        {"name": "Z LaVine", "attacking": 85, "defensive": 55},
        {"name": "K Thompson", "attacking": 88, "defensive": 75} 
    ],
    "SF": [
        {"name": "L James", "attacking": 100, "defensive": 90},
        {"name": "L Bird", "attacking": 98, "defensive": 85},
        {"name": "K Durant", "attacking": 98, "defensive": 78},
        {"name": "K Leonard", "attacking": 92, "defensive": 90},
        {"name": "S Pippen", "attacking": 88, "defensive": 85},
        {"name": "P George", "attacking": 90, "defensive": 80},
        {"name": "J Erving", "attacking": 92, "defensive": 70},
        {"name": "J Worthy", "attacking": 88, "defensive": 68},
        {"name": "V Carter", "attacking": 80, "defensive": 55},
        {"name": "D Wilkins", "attacking": 77, "defensive": 60}
    ],
    "PF": [
        {"name": "T Duncan", "attacking": 94, "defensive": 97},
        {"name": "K Garnett", "attacking": 90, "defensive": 88},
        {"name": "D Nowitzki", "attacking": 95, "defensive": 60},
        {"name": "D Rodman", "attacking": 70, "defensive": 100},
        {"name": "K Malone", "attacking": 94, "defensive": 75},
        {"name": "C Webber", "attacking": 88, "defensive": 70},
        {"name": "J Jackson Jr.", "attacking": 85, "defensive": 80},
        {"name": "B Adebayo", "attacking": 86, "defensive": 85},
        {"name": "P Siakam", "attacking": 75, "defensive": 60},
        {"name": "Z Randolph", "attacking": 80, "defensive": 72}  
    ],
    "C": [
        {"name": "K Abdul-Jabbar", "attacking": 100, "defensive": 92},
        {"name": "H Olajuwon", "attacking": 92, "defensive": 95},
        {"name": "Shaq O'Neal", "attacking": 97, "defensive": 80},
        {"name": "W Chamberlain", "attacking": 100, "defensive": 85},
        {"name": "B Russell", "attacking": 80, "defensive": 100},
        {"name": "P Ewing", "attacking": 88, "defensive": 80},
        {"name": "D Robinson", "attacking": 90, "defensive": 85},
        {"name": "A Mourning", "attacking": 85, "defensive": 88},
        {"name": "D Howard", "attacking": 70, "defensive": 75},
        {"name": "J Embiid", "attacking": 92, "defensive": 85}
    ]
}

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404 

@app.route('/debug_session')
def debug_session():
    return jsonify(dict(session))  # Convert session data to JSON and return it

@app.route('/clear-session')
def clear_session():
    keys_to_remove = ["lagA", "lagB"]  
    for key in keys_to_remove:
        session.pop(key, None)  
    simulation_state.update({
        "has_run": False,
        "scores": {"Score_lagA": 0, "Score_lagB": 0},
        "logs": [],
        "player_points": {}
    })
    return redirect(url_for('draft'))

@app.route('/')
def hjemside():
    cookies_accepted = request.cookies.get('cookiesAccepted')
    if "username1" in request.cookies and "player1" not in session:
        username1 = request.cookies.get('username1')
        session['player1'] = username1
            
    if "username2" in request.cookies and "player2" not in session:
        username2 = request.cookies.get('username2')
        session['player2'] = username2

    return render_template('hjemside.html', cookies_accepted = cookies_accepted)

@app.route("/accept-cookies")
def accept_cookies():
    response = make_response("Cookies Accepted")
    response.set_cookie("cookiesAccepted", "true", max_age=60*60*24, path="/")
    return response



@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        encrypted_email = fernet.encrypt(email.encode())
 
        new_user = User(brukernavn=username, passord=hashed_password, email = encrypted_email)
        db.session.add(new_user)
        db.session.commit()  # Save user to database

        # Get newly created user ID
        user_id = new_user.id

        # Add to Leaderboard
        new_entry = Leaderboard(user_id=user_id, antall_seire=0)
        db.session.add(new_entry)
        db.session.commit()

        print("Ny bruker registrert")
        return render_template("hjemside.html")

    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Example DB query (adjust as needed)
        user = User.query.filter_by(brukernavn=username).first()

        if not user:
            return "Bruker ikke funnet", 401  # User not found
        
        stored_hashed_password = user.passord

        if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
            response = make_response(redirect(url_for('hjemside')))

            if "player1" not in session:
                session["player1"] = username
                response.set_cookie("username1", username, max_age=60*60*24)  # Save cookie for 1 day
            elif "player2" not in session:
                session["player2"] = username
                response.set_cookie("username2", username, max_age=60*60*24)
            else:
                return "Maks spillegrense nådd"

            return response  # Redirect with cookie stored

    return render_template("login.html")  # Show login page for GET requests

@app.route('/logout_player1')
def logout_player1():
    session.pop('player1', None)
    response = make_response(render_template('logout.html', message="You have been logged out.")) 
    response.set_cookie('username1', '', expires=0)

    return response

@app.route('/logout_player2')
def logout_player2():
    session.pop('player2', None)
    response = make_response(render_template('logout.html', message="You have been logged out.")) 
    response.set_cookie('username2', '', expires=0)
    return response




@app.route('/get_players')
def get_players():
    return jsonify({
        "player1": session.get("player1", "Not logged in"),
        "player2": session.get("player2", "Not logged in")
    }) 

@app.route('/submit_team_name', methods=['POST'])
def submit_lagnavn():
    data = request.get_json()

    navn_lagA = data.get("navn_lagA")
    navn_lagB = data.get("navn_lagB")

    session['navn_lagA'] = navn_lagA
    session['navn_lagB'] = navn_lagB

    return jsonify({"message": "Team names saved", "navn_lagA": navn_lagA, "navn_lagB": navn_lagB})

@app.route('/draft')
def draft():

    navn_lagA = session.get('navn_lagA', " ")
    navn_lagB = session.get('navn_lagB', " ")

    return render_template('draft.html', navn_lagA = navn_lagA, navn_lagB = navn_lagB)

@app.route('/privacy-policy')
def privpoli():
    return render_template('privacy-policy.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/submit', methods=['POST'])
def submit_teams():
    data = request.get_json()

    lagA = data.get("lagA")
    lagB = data.get("lagB")

    session['lagA'] = lagA
    session['lagB'] = lagB

    print(f"lag A: {lagA}")
    print(f"lag B: {lagB}")

    return jsonify({'message': 'Teams received successfully!', 'teamA': lagA, 'teamB': lagB})

@app.route('/ledertavle')
def ledertavle():
    rows = db.session.query(User.brukernavn, Leaderboard.antall_seire) \
                     .join(Leaderboard, Leaderboard.user_id == User.id) \
                     .order_by(Leaderboard.antall_seire.asc()) \
                     .all()
                                            
    
    return render_template("ledertavle.html", rows = rows)

@app.route('/karriere')
def karriere():
    username1 = session.get('player1',' ')
    username2 = session.get('player2', ' ')
    matches_player1 = db.session.query(Kamper).filter(Kamper.spiller1 == username1).all()
    matches_player2 = db.session.query(Kamper).filter(Kamper.spiller2 == username2).all()
    return render_template('karriere.html', username1 = username1, matches_player1 = matches_player1, username2 = username2, matches_player2 = matches_player2)

simulation_state = {
    "has_run": False,
    "scores": {"Score_lagA": 0, "Score_lagB": 0},
    "logs": [],
    "player_points": {}
}

@app.route('/simulering')
def simulering():
    lagA = session.get('lagA', {})
    lagB = session.get('lagB', {})
    
    navn_lagA = session.get('navn_lagA', " ")
    navn_lagB = session.get('navn_lagB', " ")

    positions = ["PG", "SG", "SF", "PF", "C"]

    # For lagA
    lagA_players = {position: None for position in positions}
    for position in positions:
        for player in basketball_players[position]:
            if player['name'] in (lagA['spiller1'], lagA['spiller2'], lagA['spiller3'], lagA['spiller4'], lagA['spiller5']):
                lagA_players[position] = player

    PGlagA, SGlagA, SFlagA, PFlagA, ClagA = (lagA_players[pos] for pos in positions)

    # For lagB
    lagB_players = {position: None for position in positions}
    for position in positions:
        for player in basketball_players[position]:
            if player['name'] in (lagB['spiller1'], lagB['spiller2'], lagB['spiller3'], lagB['spiller4'], lagB['spiller5']):
                lagB_players[position] = player

    PGlagB, SGlagB, SFlagB, PFlagB, ClagB = (lagB_players[pos] for pos in positions)

    return render_template(
        'simulering.html',
        lagA=lagA, 
        lagB=lagB, 
        Score_lagA=simulation_state["scores"]["Score_lagA"],
        Score_lagB=simulation_state["scores"]["Score_lagB"],
        kamplogg=simulation_state["logs"],
        Poeng_PGlagA=simulation_state["player_points"].get("PGlagA", 0),
        Poeng_SGlagA=simulation_state["player_points"].get("SGlagA", 0),
        Poeng_SFlagA=simulation_state["player_points"].get("SFlagA", 0),
        Poeng_PFlagA=simulation_state["player_points"].get("PFlagA", 0),
        Poeng_ClagA=simulation_state["player_points"].get("ClagA", 0),
        Poeng_PGlagB=simulation_state["player_points"].get("PGlagB", 0),
        Poeng_SGlagB=simulation_state["player_points"].get("SGlagB", 0),
        Poeng_SFlagB=simulation_state["player_points"].get("SFlagB", 0),
        Poeng_PFlagB=simulation_state["player_points"].get("PFlagB", 0),
        Poeng_ClagB=simulation_state["player_points"].get("ClagB", 0),
        PGlagA_navn=PGlagA['name'],
        SGlagA_navn=SGlagA['name'],
        SFlagA_navn=SFlagA['name'],
        PFlagA_navn=PFlagA['name'],
        ClagA_navn=ClagA['name'],
        PGlagB_navn=PGlagB['name'],
        SGlagB_navn=SGlagB['name'],
        SFlagB_navn=SFlagB['name'],
        PFlagB_navn=PFlagB['name'],
        ClagB_navn=ClagB['name'],
        navn_lagA=navn_lagA,
        navn_lagB=navn_lagB
    )

def update_lederbord(username):
    user = User.query.filter_by(brukernavn=username).first()
    if user:
        lederbord_entry = Leaderboard.query.filter_by(user_id=user.id).first()
        if lederbord_entry:
            lederbord_entry.antall_seire += 1
            db.session.commit()

def save_match():
    player1 = session.get("player1", " ")
    player2 = session.get("player2", " ")
    score = f"{session['Score_lagA']} - {session['Score_lagB']}"
    
    if session['Score_lagA'] > session['Score_lagB']:
        winner = player1
        loser = player2
    elif session['Score_lagB'] > session['Score_lagA']:
        winner = player2
        loser = player1
    else:
        winner = "UAVGJORT"
        loser = "UAVGJORT"
    
    new_match = Kamper(
        spiller1=player1,
        spiller2=player2,
        stilling=score,
        vinner=winner,
        taper=loser,
        dato=datetime.now()
    )

    db.session.add(new_match)
    db.session.commit()

@socketio.on('start_simulation')
def handle_start_simulation():

    if simulation_state["has_run"]:
        emit('game_update', {
            'Score_lagA': simulation_state["scores"]["Score_lagA"],
            'Score_lagB': simulation_state["scores"]["Score_lagB"],
            'kamplogg': simulation_state["logs"],
            'player_points': simulation_state["player_points"]
        })
        return
    
    if session.get('game_completed'):
        emit('game_already_completed')
        return
    
    lagA = session.get('lagA', {})
    lagB = session.get('lagB', {})
    
    positions = ["PG", "SG", "SF", "PF", "C"]

    # Get player objects
    lagA_players = {position: None for position in positions}
    for position in positions:
        for player in basketball_players[position]:
            if player['name'] in (lagA['spiller1'], lagA['spiller2'], lagA['spiller3'], lagA['spiller4'], lagA['spiller5']):
                lagA_players[position] = player

    PGlagA, SGlagA, SFlagA, PFlagA, ClagA = (lagA_players[pos] for pos in positions)

    lagB_players = {position: None for position in positions}
    for position in positions:
        for player in basketball_players[position]:
            if player['name'] in (lagB['spiller1'], lagB['spiller2'], lagB['spiller3'], lagB['spiller4'], lagB['spiller5']):
                lagB_players[position] = player

    PGlagB, SGlagB, SFlagB, PFlagB, ClagB = (lagB_players[pos] for pos in positions)

    # Initialize game state
    game_state = {
        'Score_lagA': 0,
        'Score_lagB': 0,
        'kamplogg': [],
        'player_points': {
            'PGlagA': 0, 'SGlagA': 0, 'SFlagA': 0, 'PFlagA': 0, 'ClagA': 0,
            'PGlagB': 0, 'SGlagB': 0, 'SFlagB': 0, 'PFlagB': 0, 'ClagB': 0
        },
        'PGlagA_navn': PGlagA['name'],
        'SGlagA_navn': SGlagA['name'],
        'SFlagA_navn': SFlagA['name'],
        'PFlagA_navn': PFlagA['name'],
        'ClagA_navn': ClagA['name'],
        'PGlagB_navn': PGlagB['name'],
        'SGlagB_navn': SGlagB['name'],
        'SFlagB_navn': SFlagB['name'],
        'PFlagB_navn': PFlagB['name'],
        'ClagB_navn': ClagB['name']
    }

    antall_spill = random.randint(80, 175)
    
    # Emit initial state
    emit('game_update', game_state)
    
    # Run the simulation with small delays between plays
    for i in range(antall_spill):
        eventlet.sleep(0.1)  # Small delay between plays
        
        spill_poisjon = random.randint(1,5)
        if spill_poisjon == 1:
            # PG vs PG action
            if i%2 == 0:  # Team A's turn
                angrep = PGlagA["attacking"]
                forsvar = int(PGlagB["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                
                if tall_for_sim <= angrep:
                    måltype = random.randint(1,3)
                    if måltype == 1:
                        game_state['kamplogg'].append(f"{PGlagA['name']} skyter over {PGlagB['name']} og scorer")
                        game_state['Score_lagA'] += 3
                        game_state['player_points']['PGlagA'] += 3
                    else:
                        game_state['kamplogg'].append(f"{PGlagA['name']} driver forbi {PGlagB['name']} og setter layupen")
                        game_state['Score_lagA'] += 2
                        game_state['player_points']['PGlagA'] += 2
                else:
                    game_state['kamplogg'].append(f"{PGlagB['name']} stjeler ballen fra {PGlagA['name']} og starter et nytt angrep")
            else:  # Team B's turn
                angrep = PGlagB["attacking"]
                forsvar = int(PGlagA["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                
                if tall_for_sim <= angrep:
                    måltype = random.randint(1,3)
                    if måltype == 1:
                        game_state['kamplogg'].append(f"{PGlagB['name']} skyter over {PGlagA['name']} og scorer")
                        game_state['Score_lagB'] += 3
                        game_state['player_points']['PGlagB'] += 3
                    else:
                        game_state['kamplogg'].append(f"{PGlagB['name']} driver forbi {PGlagA['name']} og setter layupen")
                        game_state['Score_lagB'] += 2
                        game_state['player_points']['PGlagB'] += 2
                else:
                    game_state['kamplogg'].append(f"{PGlagA['name']} stjeler ballen fra {PGlagB['name']} og starter et nytt angrep")
        
        elif spill_poisjon == 2:
            if i%2 == 0:
                angrep = SGlagA["attacking"]
                forsvar = int(SGlagB["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{SGlagA['name']} skyter en 3-er over {SGlagB['name']} og scorer")
                    game_state['Score_lagA'] += 3
                    game_state['player_points']['SGlagA'] += 3
                else:
                    game_state['kamplogg'].append(f"{SGlagB['name']} blokkerer skuddet til {SGlagA['name']} og spiller ballen fram")
            else:
                angrep = SGlagB["attacking"]
                forsvar = int(SGlagA["defensive"]-40)

                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{SGlagB['name']} skyter en 3-er over {SGlagA['name']} og scorer")
                    game_state['Score_lagB'] += 3
                    game_state['player_points']['SGlagB'] += 3
                else:
                    game_state['kamplogg'].append(f"{SGlagA['name']} blokkerer {SGlagB['name']} og spiller ballen fram")
        elif spill_poisjon == 3:
            if i%2 == 0:
                angrep = SFlagA["attacking"]
                forsvar = int(SFlagB["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{SFlagA['name']} setter ned {SFlagB['name']} og scorer")
                    mål_type = random.randint(1,5)
                    if mål_type == 1:
                        game_state['Score_lagA'] += 3
                        game_state['player_points']['SFlagA'] += 3
                    else:
                        game_state['Score_lagA'] += 2
                        game_state['player_points']['SFlagA'] += 2
                else:
                    game_state['kamplogg'].append(f"{SFlagB['name']} tar ballen fra {SFlagA['name']} og dribbler oppover")
            else:
                angrep = SFlagB["attacking"]
                forsvar = int(SGlagA["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{SFlagB['name']} setter ned {SFlagA['name']} og scorer")
                    mål_type = random.randint(1,5)
                    if mål_type == 1:
                        game_state['Score_lagB'] += 3
                        game_state['player_points']['SFlagB'] += 3
                    else:
                        game_state['Score_lagB'] += 2
                        game_state['player_points']['SFlagB'] += 2
                else:
                    game_state['kamplogg'].append(f"{SFlagA['name']} tar ballen fra {SFlagB['name']} og dribbler oppover")
        elif spill_poisjon == 4:
            if i%2 == 0:
                angrep = PFlagA["attacking"]
                forsvar = int(PFlagB["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{PFlagA['name']} finter ut {PFlagB['name']} og scorer")
                    game_state['Score_lagA'] += 2
                    game_state['player_points']['PFlagA'] += 2
                else:
                    game_state['kamplogg'].append(f"{PFlagB['name']} stjeler ballen fra {PFlagA['name']} og spiller ballen fra seg")
            else:
                angrep = PFlagB["attacking"]
                forsvar = int(PFlagA["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{PFlagB['name']} finter ut {PFlagA['name']} og scorer")
                    game_state['Score_lagB'] += 2
                    game_state['player_points']['PFlagB'] += 2
                else:
                    game_state['kamplogg'].append(f"{PFlagA['name']} stjeler ballen fra {PFlagB['name']} og spiller ballen fra seg")
        elif spill_poisjon == 5:
            if i%2 == 0:
                angrep = ClagA["attacking"]
                forsvar = int(ClagB["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{ClagA['name']} dunker på {ClagB['name']}")
                    game_state['Score_lagA'] += 2
                    game_state['player_points']['ClagA'] += 2
                else:
                    game_state['kamplogg'].append(f"{ClagB['name']} vinner rebound mot {ClagA['name']} og spiller ballen fra seg")
            else:
                angrep = ClagB["attacking"]
                forsvar = int(ClagA["defensive"]-40)
                tall_for_sim = random.randint(1, angrep + forsvar)
                if tall_for_sim <= angrep:
                    game_state['kamplogg'].append(f"{ClagB['name']} dunker på {ClagA['name']}")
                    game_state['Score_lagB'] += 2
                    game_state['player_points']['ClagB'] += 2
                else:
                    game_state['kamplogg'].append(f"{ClagA['name']} vinner rebound mot {ClagB['name']} og spiller ballen fra seg")
        # Emit update after each play
        emit('game_update', game_state)
    
    # Final game over message
    game_state['kamplogg'].append(f"Tiden er ute, sluttstilling {game_state['Score_lagA']} - {game_state['Score_lagB']}")
    emit('game_update', game_state)
    
    simulation_state.update({
        "has_run": True,
        "scores": {
            "Score_lagA": game_state["Score_lagA"],
            "Score_lagB": game_state["Score_lagB"]
        },
        "logs": game_state["kamplogg"],
        "player_points": game_state["player_points"]
    })
    
    # Update leaderboard and save match
    if "player1" in session and game_state['Score_lagA'] > game_state['Score_lagB']:
        update_lederbord(session['player1'])
    elif "player2" in session and game_state['Score_lagA'] < game_state['Score_lagB']:
        update_lederbord(session['player2'])
    
    if "player1" and "player2" in session:
        save_match()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=3030)