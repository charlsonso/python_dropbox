import unittest
from python_dropbox.app.app_runner import app_runner
import os
from python_dropbox.app.credential_checker import get_service
import shutil

def setup():
    #create folder to watch with file upload
    os.mkdir('sample')
    with open('sample/sample.txt', 'w+') as f:
        f.write(' ')


class TestMethods(unittest.TestCase):

    def test_app_runner(self):
        setup()
        app_runner('sample', 'credentials/credentials.json', None)
        service = get_service(None, 'sample/token.pickle', 'sample')
        result = service.files().list(pageSize=10, fields="nextPageToken, files(name)").execute()
        answer = None
        files = result['files']
        for i in files:
            if i['name'] == 'sample.txt':
                answer = 'sample.txt'
    
        self.assertTrue('sample.txt', result) 
        shutil.rmtree('sample')

if __name__ == '__main__':
    unittest.main()
