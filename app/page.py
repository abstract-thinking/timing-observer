from flask import (
    Blueprint, render_template
)

from app.db import get_db

bp = Blueprint('page', __name__)


@bp.route('/indices')
def indices():
    db = get_db()
    codes = db.execute(
        'SELECT * from indices'
    ).fetchall()
    return render_template('page/indices.html', indices=codes)


@bp.route('/quotes')
def show_quotes():
    db = get_db()
    quotes = db.execute(
        'SELECT * from quotes'
    ).fetchall()
    return render_template('page/quotes.html', quotes=quotes)


# https://stackoverflow.com/questions/29855081/how-to-get-a-list-of-dates-from-a-week-number-in-python
@bp.route('/rsl')
def rsl():
    db = get_db()
    quote = db.execute(
        """SELECT avg(rsl) AS "RSL" FROM quotes WHERE quotes.date_id IN 
        (SELECT id FROM dates WHERE date > (SELECT DATETIME('now', '-3 day')))"""
    ).fetchone()
    return render_template('page/rsl.html', quote=quote)


@bp.route('/gi')
def indicate():
    db = get_db()
    gi = db.execute("""SELECT * FROM germany_indicator WHERE date > '1970-01-01'""").fetchall()

    return render_template("page/gi.html", gi=gi)
