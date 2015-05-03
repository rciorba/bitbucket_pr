# pylint: disable=protected-access, bad-continuation, line-too-long
from mock import patch

import bitbucket_pr


mock_data = {}
mock_data['pullrequests'] = {
 'page': 1,
 'pagelen': 10,
 'size': 1,
 'values': [{'author': {'display_name': 'Radu Ciorba',
    'links': {'avatar': {'href': 'https://secure.gravatar.com/avatar/27f39fbb956a55b378a23cb3a0b66fc6?d=https%3A%2F%2Fd3oaxc4q5k2d6q.cloudfront.net%2Fm%2F9c586b5d8b1e%2Fimg%2Fdefault_avatar%2F32%2Fuser_blue.png&s=32'},
     'html': {'href': 'https://bitbucket.org/raduciorba'},
     'self': {'href': 'https://api.bitbucket.org/2.0/users/raduciorba'}},
    'username': 'raduciorba',
    'uuid': '{88131523-3d88-4e76-b540-a4b56808a5c3}'},
   'close_source_branch': False,
   'closed_by': None,
   'created_on': '2015-05-02T17:47:33.167321+00:00',
   'description': '',
   'destination': {'branch': {'name': 'default'},
    'commit': {'hash': '0dc895df4b4f',
     'links': {'self': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/commit/0dc895df4b4f'}}},
    'repository': {'full_name': 'raduciorba/pylint',
     'links': {'avatar': {'href': 'https://d3oaxc4q5k2d6q.cloudfront.net/m/9c586b5d8b1e/img/language-avatars/default_16.png'},
      'html': {'href': 'https://bitbucket.org/raduciorba/pylint'},
      'self': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint'}},
     'name': 'pylint',
     'uuid': '{a056c36c-705f-4683-8679-0fa6862e88c2}'}},
   'id': 4,
   'links': {'activity': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/activity'},
    'approve': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/approve'},
    'comments': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/comments'},
    'commits': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/commits'},
    'decline': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/decline'},
    'diff': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/diff'},
    'html': {'href': 'https://bitbucket.org/raduciorba/pylint/pull-request/4'},
    'merge': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4/merge'},
    'self': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4'}},
   'merge_commit': None,
   'reason': '',
   'source': {'branch': {'name': 'test_droneio_pr'},
    'commit': {'hash': 'a1023eece883',
     'links': {'self': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/commit/a1023eece883'}}},
    'repository': {'full_name': 'raduciorba/pylint',
     'links': {'avatar': {'href': 'https://d3oaxc4q5k2d6q.cloudfront.net/m/9c586b5d8b1e/img/language-avatars/default_16.png'},
      'html': {'href': 'https://bitbucket.org/raduciorba/pylint'},
      'self': {'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint'}},
     'name': 'pylint',
     'uuid': '{a056c36c-705f-4683-8679-0fa6862e88c2}'}},
   'state': 'OPEN',
   'title': 'test pr',
   'updated_on': '2015-05-02T17:52:18.995773+00:00'}]}


class FakeResponse(object):
    """A fake response object.
    The object is callable, and returns self, so you can use
    it to patch request methods in your tests.
    """

    def __call__(self, url, data=None, auth=None):
        self.called_url = url
        self.called_data = data
        return self

    def __init__(self, code=200, data=""):
        self.status_code = code
        self.data = data
        self.called_url = None
        self.called_data = None

    def json(self):
        return self.data

    def assert_called(self, expected_url=None, expected_data=None):
        if expected_url:
            assert self.called_url == expected_url
        if expected_data:
            assert self.called_data == expected_data


def test_find_pr():
    bb = bitbucket_pr.BB(None, None)
    with patch.object(bitbucket_pr, "get", FakeResponse(data=mock_data['pullrequests'])):
        expected = {
            'href': 'https://api.bitbucket.org/2.0/repositories/raduciorba/pylint/pullrequests/4',
            'id': 4
        }
        assert bb.find_pr('test_droneio_pr') == expected


def test_post_comment():
    bb = bitbucket_pr.BB(None, None)
    response = FakeResponse()
    with patch.object(bitbucket_pr, "post", response):
        bb._post_comment("a comment", {'id': 4})
        response.assert_called(expected_data={"content": "a comment"})
