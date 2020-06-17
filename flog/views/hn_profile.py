from flask import Blueprint, request, render_template

from flog.libs.hackernews import hn_process_profile, hn_fetch_profile

ident = 'hn-profile'

bp = Blueprint(ident, __name__)


@bp.route(f'/{ident}', methods=('GET', 'POST'))
def hn_profile():
    if request.method == 'GET':
        return render_template('hn-profile.html')

    username = request.form['username']
    profile = hn_fetch_profile(username)
    subcount, karma = hn_process_profile(profile)

    return f'HackerNews user {username} has {subcount} submissions and' \
        f' {karma} karma.'


