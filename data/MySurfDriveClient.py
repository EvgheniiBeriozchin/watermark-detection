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


# Download only images in specific folder - change this to WZ_II_Thueringen and directory to final directory

my_surfdrive_client = MySurfDriveClient()
root_content_list = my_surfdrive_client.list_content()
print(root_content_list)

for entry in root_content_list:
    if entry.endswith('WZ_II_Thueringen/'):
        print('Inhalt von WZ_II_Thueringen:', entry)
        os.mkdir('./' + entry)
        subfolder_content_list = my_surfdrive_client.list_content(entry)
        for entry_sub in subfolder_content_list:
            file_list = my_surfdrive_client.list_content(entry_sub)
            os.mkdir('./' + entry_sub)
            for f in file_list:
                if not f.endswith('/'):
                    file_name = os.path.basename(f)
                    my_surfdrive_client.get_file_from_remote(f, './' + f)
            print(subfolder_content_list)

my_surfdrive_client.logout()
