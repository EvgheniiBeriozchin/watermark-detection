import nextcloud_client
import os

SURFDRIVE_WBDAV_URL = 'https://surfdrive.surf.nl/files/'
SURFDRIVE_SHARE_TOKEN = 'WAFZCEsoWYVNWLJ'


class MySurfDriveClient:
    """"This class supports downloading files and folder structures from surfdrive"""
    def __init__(self, url=SURFDRIVE_WBDAV_URL, user=SURFDRIVE_SHARE_TOKEN, passwd=""):
        self.url = url
        self.user = user  # User equals 15-byte share token at anonymous login
        self.passwd = passwd
        self.nc = nextcloud_client.Client(self.url, debug=True)
        self.annon_login()

    def __del__(self):
        print('logout...')
        self.logout()

    def annon_login(self):
        self.nc.anon_login(self.user, self.passwd)

    def logout(self):
        self.nc.logout()

    def list_content(self, path='/') -> list:
        file_list = self.nc.list(path)
        return [e.path for e in file_list]

    def get_file_from_remote(self, remote_file, local_file):
        self.nc.get_file(remote_file, local_file)


