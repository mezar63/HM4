import sqlite3

from flask import Flask, render_template

from seting import seting_customers, seting_tracks

app = Flask(__name__)


@app.route('/')
def main_page():
    return (
        "<p>Для создания данных базы /setup/"
        "<p>Увидеть кол-во уникальных имен /names/"
        "<p>Увидеть кол-во треков в базе /tracks/"
        "<p>Увидеть информацию о треках /tracks-sec/"

    )


@app.route('/setup/')
def setups():
    seting_customers()
    seting_tracks()

    return "Вы создали данные для базы данных flask"


@app.route('/names/', methods=['GET'])
def get_customer_name():
    with sqlite3.connect('flask.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(DISTINCT first_name) FROM customers")
        customers = cur.fetchall()
        names_counter = len(customers)

        return render_template('customers.html', names_counter=names_counter, customers=customers)


@app.route('/tracks/', methods=['GET'])
def get_count_records_tracks():
    with sqlite3.connect('flask.db') as conn:
        cur = conn.cursor()
        cur.execute(""" SELECT id FROM tracks """)
        tracks = cur.fetchall()
        tracks_counter = len(tracks)

        return render_template('count_traks.html', tracks_counter=tracks_counter, tracks=tracks)


@app.route('/tracks-sec/', methods=['GET'])
def get_tracks_information():
    with sqlite3.connect('flask.db') as conn:
        cur = conn.cursor()
        cur.execute(""" SELECT id, singer, track_name, track_length, release_date FROM tracks """)
        tracks = cur.fetchall()

        return render_template('tracks_information.html', tracks=tracks)


@app.errorhandler(404)
def error_404(error):
    return '<h1 style="text-align:center; font-size:24px;">Вы сделали что-то не так(</h1>'


if __name__ == "__main__":
    app.run(debug=True)
