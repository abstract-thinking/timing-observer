import pendulum
from flask import Blueprint, render_template

from app.db import get_db

bp = Blueprint('page', __name__)


@bp.route('/indices')
def show_indices():
    db = get_db()

    indices = db.execute(
        'SELECT * from indices'
    ).fetchall()

    return render_template('page/indices.html', indices=indices)


@bp.route('/quotes')
def show_quotes():
    db = get_db()

    quotes = db.execute(
        'SELECT * from quotes, indices, dates WHERE quotes.code_id = indices.id AND quotes.date_id = dates.id ORDER BY date DESC'
    ).fetchall()

    return render_template('page/quotes.html', quotes=quotes)


@bp.route('/rsl')
def show_rsl():
    db = get_db()

    today = pendulum.now().start_of('week')

    result = []
    for weeks in range(0, 52):
        week = today.subtract(weeks=weeks)
        first_day_of_week = week.start_of('week').to_date_string()
        end_day_of_week = week.end_of('week').to_date_string()

        sql = "SELECT avg(rsl) AS 'RSL' FROM quotes WHERE quotes.date_id IN (" \
              "SELECT id FROM dates WHERE date BETWEEN '{}' AND '{}')".format(first_day_of_week, end_day_of_week)
        rsl = db.execute(sql).fetchone()[0]

        result.append((first_day_of_week, end_day_of_week, rsl))

    return render_template('page/rsl.html', result=result)


@bp.route('/gi')
def show_gi():
    db = get_db()

    gi = db.execute(
        """SELECT * FROM germany_indicator WHERE date > '1970-01-01' ORDER BY date DESC""").fetchall()

    return render_template('page/gi.html', gi=gi)
