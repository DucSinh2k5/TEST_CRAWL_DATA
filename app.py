import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_NAME = 'premier_league.db'

def db_connection():
    """Tạo kết nối SQLite và trả về đối tượng kết nối."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Trả về dạng dict
    return conn


@app.route('/')
def index():
    return """
    <h2>Premier League REST API</h2>
    <ul>
        <li>/api/player?name=TÊN_CẦU_THỦ → Tra cứu theo tên</li>
        <li>/api/club?squad=TÊN_CLB → Tra cứu theo câu lạc bộ</li>
    </ul>
    """


@app.route('/api/player', methods=['GET'])
def get_player_by_name():
    """Trả về toàn bộ chỉ số cầu thủ theo tên."""
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Thiếu tham số "name"'}), 400

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cau_Thu WHERE Name LIKE ?", (f"%{name}%",))
    players = cursor.fetchall()
    conn.close()

    if not players:
        return jsonify({'message': 'Không tìm thấy cầu thủ nào'}), 404

    return jsonify([dict(p) for p in players])


@app.route('/api/club', methods=['GET'])
def get_players_by_club():
    """Trả về danh sách cầu thủ của CLB."""
    squad = request.args.get('squad')
    if not squad:
        return jsonify({'error': 'Thiếu tham số "squad"'}), 400

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cau_Thu WHERE Team LIKE ?", (f"%{squad}%",))
    players = cursor.fetchall()
    conn.close()

    if not players:
        return jsonify({'message': 'Không tìm thấy CLB'}), 404

    return jsonify([dict(p) for p in players])


if __name__ == '__main__':
    app.run(debug=True, port=5000)


