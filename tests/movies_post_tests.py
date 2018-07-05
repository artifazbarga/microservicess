import unittest

import flask
import requests
import json
import sys

from services import main
from services.main import ROOT_MOVIES


class TestMoviesService(unittest.TestCase):
    def setUp(self):
        self.app = main.app.test_client()

    def test_get_root(self):
        response = self.app.get('/')
        self.assertEqual(json.loads(response.get_data().decode(sys.getdefaultencoding())),
                         ROOT_MOVIES)

    def test_add_movie(self):
        response = self.app.post('/movies', data=dict(
            director='Tomer Admon',
            rating='9.3',
            title='TEST MOVIE'
            ), follow_redirects=True)
        self.assertIn('TEST MOVIE',
                      str(json.loads(response.get_data().decode(sys.getdefaultencoding()))))



if __name__ == "__main__":
    unittest.main()