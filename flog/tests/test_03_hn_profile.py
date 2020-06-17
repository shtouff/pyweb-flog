"""
    Principle #3: make tests as close to the "real world" as possible
    Principle #4: it's helpful to refactor code to make it easier to test
    Principle #5: use mocking as needed to avoid depending on the "real world" for data

    The tests below are effective, but brittle.  If the source data changes (e.g. I submit another
    comment on HN or my karma goes up) or there is a network blip, the second test will fail.

    Additionally, the first test passes but misses a bug.  Run the flask web server and submit
    a user name and you will find a bug.

    Exercises (create a new test file and a new view file):

    1. Refactor the view to use a two step process to get and then process the user profile data
        - write a test for hn_process_profile()
        - write stub functions
        - refactor view to use stub functions (current tests should not break)
    2. Use [patch] to mock out hn_fetch_profile()
        - it's a good idea to provide different data than live, to make sure your mock is working
    3. Use [responses] to test hn_fetch_profile()
    4. Use the [Webtest] library to do better form handling tests that expose the bug in our view
        - You will probably want to use a pytest fixture to load the webtest client when needed
           (see conftest.py for example)
        - This will result in a single test for your view, handling both GET & POST in the same test
        - Fix the bug

    [webtest]: https://docs.pylonsproject.org/projects/webtest/
    [patch]: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
    [responses]: https://github.com/getsentry/responses
"""
from unittest.mock import patch

import pytest
import responses
from webtest import TestApp

from flog.libs.hackernews import hn_process_profile, hn_fetch_profile


@pytest.fixture()
def profile():
    return {
        "karma": 42,
        "submitted": [
            'un',
            'deux',
            'trois',
        ]
    }


@pytest.fixture()
def wt(app):
    return TestApp(app)


class Tests:
    @patch('flog.views.hn_profile.hn_fetch_profile')
    def test_form(self, mock, wt, profile):
        mock.return_value = profile

        resp = wt.get('/hn-profile')
        assert resp.status_code == 200
        assert b'Please enter a Hacker News username:' in resp.body

        resp.form['username'] = 'rsyring'
        resp = resp.form.submit()

        assert mock.called
        assert resp.status_code == 200
        assert b'HackerNews user rsyring has 3 submissions and 42 karma.' in resp.body

    @responses.activate
    def test_hn_fetch_profile(self, profile):
        username = "rsysring"
        responses.add(
            responses.GET,
            f'https://hacker-news.firebaseio.com/v0/user/{username}.json',
            json=profile, status=200
        )

        fetched_profile = hn_fetch_profile(username)
        assert "karma" in fetched_profile
        assert "submitted" in fetched_profile

    def test_hn_process_profile(self, profile):
        subcount, karma = hn_process_profile(profile)
        assert subcount == 3
        assert karma == 42
