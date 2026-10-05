import random
from flask import Flask, render_template, jsonify, session

app = Flask(__name__)
app.secret_key = 'super_tajny_klucz_cs2'

KNIVES = [
    {
        'id': 'emerald',
        'name': '★ Karambit | Gamma Doppler Emerald',
        'rarity': 'Emerald (10%)',
        'color': '#2ecc71',
        'chance': 10,
        'img': 'https://img.icons8.com/color/96/dagger.png'
    },  # <--- TUTAJ MUSI BYĆ PRZECINEK!
    {
        'id': 'starozytne-kroniki',
        'name': '⚔️ Nóż Taktyczny | Starożytne Kroniki',
        'rarity': 'Starożytne Kroniki (30%)',
        'color': '#f1c40f',
        'chance': 30,
        'img': 'https://img.icons8.com/color/96/sword.png'
    },  # <--- TUTAJ TEŻ MUSI BYĆ PRZECINEK!
    {
        'id': 'czerwona-siatka',
        'name': '⚔️ Nóż Taktyczny | Czerwona Siatka Technologiczna',
        'rarity': 'Czerwona Siatka (60%)',
        'color': '#e74c3c',
        'chance': 60,
        'img': 'https://img.icons8.com/color/96/pocket-knife.png'
    }
]
@app.route('/')
def home():
    if 'inventory' not in session:
        session['inventory'] = []
    if 'crates_count' not in session:
        session['crates_count'] = 0
    return render_template('index.html', inventory=session['inventory'], crates_count=session['crates_count'])

@app.route('/buy_crate', methods=['POST'])
def buy_crate():
    session['crates_count'] = session.get('crates_count', 0) + 1
    return jsonify({'status': 'ok', 'crates_count': session['crates_count']})

@app.route('/open_spin', methods=['POST'])
def open_spin():
    crates = session.get('crates_count', 0)
    if crates <= 0:
        return jsonify({'error': 'Brak skrzynek w ekwipunku!'}), 400
    
    session['crates_count'] = crates - 1

    weights = [k['chance'] for k in KNIVES]
    won_knife = random.choices(KNIVES, weights=weights, k=1)[0]
    
    inventory = session.get('inventory', [])
    inventory.insert(0, won_knife)
    session['inventory'] = inventory
    
    return jsonify({
        'knife': won_knife,
        'remaining_crates': session['crates_count']
    })

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)