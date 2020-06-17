import contextlib
from unittest import mock

import requests


def fetch_profile(username):
    url = f'https://hacker-news.firebaseio.com/v0/user/{username}.json'
    return requests.get(url, timeout=2.0).json()


def process_profile(profile_data):
    subcount = len(profile_data['submitted'])

    return subcount, profile_data["karma"]


def profile_stats(username, use_html):
    profile = fetch_profile(username)

    styled_username = f'<strong>{username}</strong>' if use_html else username

    if profile is None:
        return f'No HackerNews user: {styled_username}'

    subcount, karma = process_profile(profile)

    return f'HackerNews user {styled_username} has {subcount} submissions and' \
        f' {karma} karma.'


@contextlib.contextmanager
def mock_profile(karma=None, submitted=[1, 2, 3]):
    with mock.patch('flog.libs.hackernews.fetch_profile', autospec=True, spec_set=True) \
            as m_fetch_profile:
        m_fetch_profile.return_value = None if karma is None else {
            'karma': karma,
            'submitted': submitted
        }
        yield