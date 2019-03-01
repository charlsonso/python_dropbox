# iBox
## Python CLI Application for uploading items to the drive

Currently in alpha. Tested on OSX 10.11.16 on Python 3.7.0

### Installation
1. Clone repository  
``` git clone git@github.com:so0p/python_dropbox.git ```

2. Navigate into the repo and install application  
``` python setup.py install ```

### How To
1. Navigate to ```https://developers.google.com/drive/api/v3/quickstart/python``` and follow step one. Download credentials.json by clicking <b> Download Client Configuration </b>

2. For the first time use, use the command line option --credential in order to download pickle file.  
``` ibox UPLOAD_DIR --credential path/to/credentials.json```

3. After the credential file has been properly loaded, a token.pickle should exist within your upload directory. Now use the command  
``` ibox UPLOAD_DIR --token path_to/token.pickle ```
to use the cloud application.

### Run Tests
1. Navigate into the repo and test the application with  
```python setup.py test ```  
This will run tests integrated into the build package similar to Maven in Java.

### Known Bugs
* Trash must be cleared from Google Drive for items to be deleted/ignored .
* Modified Files for updating is currently causing files to be repeatdly uploaded and downloaded.
* token.pickle should be a hidden file and checked automatically instead of a command line option.


