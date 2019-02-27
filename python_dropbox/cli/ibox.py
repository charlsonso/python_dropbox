import argparse
from python_dropbox.app.app_runner import app_runner
def get_args():
    parser = argparse.ArgumentParser(description='Sync files from specified folder to a Google Drive.')
    parser.add_argument('folder', type=str, help='Folder to sync to Google Drive')
    parser.add_argument('--credentials', type=str, help='Location to Credential File')
    parser.add_argument('--pickle', type=str, help='Location to Pickle File')
    return parser

def main():
    args = get_args().parse_args()
    app_runner(args.folder, args.credentials, args.pickle)

if __name__ == '__main__':
    main()

