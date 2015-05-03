import argparse

from requests import get, post
from requests.auth import HTTPBasicAuth


class BB(object):
    base = "https://api.bitbucket.org/"

    def __init__(self, user, password):
        self.auth = HTTPBasicAuth(user, password)

    def find_pr(self, branch):
        resp = get(self.base + "/2.0/repositories/raduciorba/pylint/pullrequests/", auth=self.auth)
        assert resp.status_code == 200
        data = resp.json()
        for pr in data['values']:
            if pr['source']['branch']['name'] == branch:
                return {
                    'id': pr['id'],
                    'href': pr['links']['self']['href']}

    def post_comment(self, message, branch):
        pull_request = self.find_pr(branch)
        return self._post_comment(message, pull_request)

    def _post_comment(self, message, pull_request):
        pull_request_id = pull_request['id']
        url = "{}1.0/repositories/raduciorba/pylint/pullrequests/{}/comments/".format(
            self.base, pull_request_id)
        resp = post(url, data={"content": message}, auth=self.auth)
        assert resp.status_code == 200
        return resp


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="The bitbucket username.")
    parser.add_argument("-p", "--password", help="The bitbucket password.")
    parser.add_argument("-m", "--message", help="Message to post.")
    parser.add_argument("-b", "--branch", help="Branch the tests were ran against.")
    args = parser.parse_args()
    bb = BB(args.user, args.password)
    bb.post_comment(args.message, args.branch)
