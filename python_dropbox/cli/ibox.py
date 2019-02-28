import argparse
from python_dropbox.app.app_runner import app_runner
import os
def get_args():
    parser = argparse.ArgumentParser(description='Sync files from specified folder to a Google Drive.')
    parser.add_argument('folder', type=str, help='Folder to sync to Google Drive')
    parser.add_argument('--credential', type=str, help='Location to Credential File')
    parser.add_argument('--pickle', type=str, help='Location to Pickle File')
    return parser

def main():
    args = get_args().parse_args()
    if not os.path.exists(os.path.abspath(args.folder)):
        raise Exception('Target Folder does not exist')

    app_runner(os.path.abspath(args.folder), 
               args.credential,
               args.pickle)

if __name__ == '__main__':
    main()

