import connection
from flask import Blueprint, request, jsonify
from connection import get_connection

load_player_bp = Blueprint('load_player', __name__)
yhteys = get_connection()


@load_player_bp.route('/loadPlayer', methods=['GET'])
def load_player():
    pelaajan_nimi = request.args.get('name')
    kursori = yhteys.cursor()
    kursori.execute(f"SELECT player.id, screen_name, location, airport.name FROM player, airport WHERE player.location = airport.ident AND screen_name = '{pelaajan_nimi}'")
    tulos = kursori.fetchone()
    kursori.close()

    if tulos:
        pelaajan_data = {
            'id': tulos[0],
            'screen_name': tulos[1],
            'location': tulos[2],
            'location_name': tulos[3]
        }
        return jsonify(pelaajan_data), 200
    else:
        pelaajan_data = {'virhe': 'Pelaajaa ei löydy'}
        return jsonify(pelaajan_data), 200
