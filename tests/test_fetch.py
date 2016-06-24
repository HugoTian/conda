import unittest
from conda import fetch
import  random
import responses

def generate_random_path():
    return '/some/path/to/file%s' % random.randint(100, 200)

class download_Testcase(unittest.TestCase):
    def test_download_404(self):
         with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'http://twitter.com/api/1/foobar',
                 body='{}', status=200,
                 content_type='application/json')
            resp = requests.get('http://twitter.com/api/1/foobar')

        assert resp.status_code == 200

    # outside the context manager requests will hit the remote server
    resp = requests.get('http://twitter.com/api/1/foobar')
    resp.status_code == 404