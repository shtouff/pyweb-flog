from flask import Blueprint, request, render_template
import requests

ident = 'hn-profile'

bp = Blueprint(ident, __name__)


def hn_process_profile(profile):
    return len(profile['submitted']), profile['karma']


def hn_fetch_profile(username):
    url = f'https://hacker-news.firebaseio.com/v0/user/{username}.json'
    profile = requests.get(url, timeout=2.0).json()
    return profile


@bp.route(f'/{ident}', methods=('GET', 'POST'))
def hn_profile():
    if request.method == 'GET':
        return render_template('hn-profile.html')

    username = request.form['username']
    profile = hn_fetch_profile(username)
    subcount, karma = hn_process_profile(profile)

    return f'HackerNews user {username} has {subcount} submissions and' \
        f' {karma} karma.'


