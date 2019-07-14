import pendulum
from flask import Blueprint, render_template

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


@bp.route('/rsl')
def rsl():
    db = get_db()

    today = pendulum.now().start_of('week')

    result = []
    for weeks in range(0, 52):
        period = today - today.subtract(weeks=weeks)

        sql = "SELECT avg(rsl) AS 'RSL' FROM quotes WHERE quotes.date_id IN (" \
              "SELECT id FROM dates WHERE date BETWEEN '{}' AND '{}')".format(period.start, period.end)
        rsl = db.execute(sql).fetchone()[0]

        result.append((period.start, period.end, rsl))

    return render_template('page/rsl.html', result=result)


@bp.route('/gi')
def gi():
    db = get_db()

    germany_indicator = db.execute(
        """SELECT * FROM germany_indicator WHERE date > '1970-01-01' ORDER BY date DESC""").fetchall()

    return render_template('page/gi.html', gi=germany_indicator)
