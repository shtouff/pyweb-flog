import requests


def process_profile(profile):
    return len(profile['submitted']), profile['karma']


def fetch_profile(username):
    url = f'https://hacker-news.firebaseio.com/v0/user/{username}.json'
    profile = requests.get(url, timeout=2.0).json()
    return profile


def profile_stats(username, web):
    profile = fetch_profile(username)

    if profile is None:
        return f'HackerNews user {username} not found.'

    count, karma = process_profile(profile)
    if web:
        username = f'<strong>{username}</strong>'
    return f'HackerNews user {username} has {count} submissions and {karma} karma.'
