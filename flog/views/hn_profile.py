from flask import Blueprint, request, render_template

from flog.libs.hackernews import profile_stats

ident = 'hn-profile'

bp = Blueprint(ident, __name__)


@bp.route(f'/{ident}', methods=('GET', 'POST'))
def hn_profile():
    if request.method == 'GET':
        return render_template('hn-profile.html')

    return profile_stats(request.form['username'], True)
