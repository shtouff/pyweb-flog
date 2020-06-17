import requests


def hn_process_profile(profile):
    return len(profile['submitted']), profile['karma']


def hn_fetch_profile(username):
    url = f'https://hacker-news.firebaseio.com/v0/user/{username}.json'
    profile = requests.get(url, timeout=2.0).json()
    return profile