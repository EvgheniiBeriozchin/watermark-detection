# Download only images in specific folder - change this to WZ_II_Thueringen and directory to final directory
import os
from MySurfDriveClient import MySurfDriveClient


my_surfdrive_client = MySurfDriveClient()
root_content_list = my_surfdrive_client.list_content()
dir = '/home/watermarks/watermarks-project/data/dnb_raw/'


for entry in root_content_list:
    if entry.endswith('WZ_II_Thueringen/'):
        print('Inhalt von WZ_II_Thueringen:', entry)
        dir_path = dir + entry

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        subfolder_content_list = my_surfdrive_client.list_content(entry)
        for entry_sub in subfolder_content_list:
            subfolder_path = dir + entry_sub

            if not os.path.exists(subfolder_path):
                os.mkdir(subfolder_path)

            if entry_sub.endswith('WZ-II-380/'):
                print('Inhalt WZ-II-380')
                subsub_folder = my_surfdrive_client.list_content(entry_sub)

                for ent in subsub_folder:
                    subsub_path = dir + ent

                    if not os.path.exists(subsub_path):
                        os.mkdir(subsub_path)

                    sub_files = my_surfdrive_client.list_content(ent)
                    for file in sub_files:
                        if not file.endswith('/'):
                            file_name = os.path.basename(file)
                            file_path = dir + file

                            if not os.path.exists(file_path):
                                    my_surfdrive_client.get_file_from_remote(file, file_path)

            file_list = my_surfdrive_client.list_content(entry_sub)
            for f in file_list:
                if not f.endswith('/'):
                    file_name = os.path.basename(f)
                    file_path = dir + f

                    if not os.path.exists(file_path):
                        my_surfdrive_client.get_file_from_remote(f, file_path)


print("Download finished")
my_surfdrive_client.logout()
