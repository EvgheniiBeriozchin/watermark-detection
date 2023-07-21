import os
import numpy as np
import pandas as pd

i


def get_test_paths(rootdir):
    classlabel = []

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                fullpath = os.path.join(subdir, file)
                classpath = os.path.dirname(fullpath)
                folderpath = os.path.dirname(classpath)

                classlabel.append([os.path.join(os.path.basename(folderpath), file), os.path.basename(classpath)])

    return classlabel


def get_images_in_df(path):
    files = os.listdir(path)
    df = pd.DataFrame(files, columns=["Path"])
    df[["im_name", "rest"]] = df['Path'].str.split('-', 1, expand=True)
    df[["rest", "position", "jpg"]] = df['rest'].str.split('.', 0, expand=True)
    df[["png", "position"]] = df['position'].str.split('_', 2, expand=True)
    return df


def process_result(path_results):
    test_lables = pd.read_csv("TestSetLabels.csv")
    test_lables[["Path", "im_name"]] = test_lables['Path'].str.split('/', 1, expand=True)
    test_lables[["im_name", "rest"]] = test_lables['im_name'].str.split('.', 1, expand=True)
    test_lables["im_name"] = test_lables['im_name'].str.split('-', 1, expand=True)[0]

    dir_list = os.listdir(path_results)
    for line in dir_list:
        if not line.endswith('outputs'):
            dir_list.remove(line)

    target_images = pd.DataFrame(dir_list, columns=["path"])

    target_images[["im_name", "rest"]] = target_images['path'].str.split('-', 1, expand=True)
    target_images[['match', 'name_match']] = 0
    full_db = target_images.merge(test_lables, on="im_name")
    for i, image_path in enumerate(full_db.path):
        path_i = os.path.join(path_results, image_path)
        get = get_images_in_df(path_i)
        get = get.sort_values(by='position')
        mask = get.im_name.isin(full_db.im_name[full_db.Class == full_db.Class[i]])
        full_db.match[i] = get.position[mask].to_string(index=False)
        full_db.name_match[i] = get.im_name[mask].to_string(index=False)

    full_db.sort_values(by='im_name')
    return full_db


def get_accuracy(excel_path, sheetname, write_csv=False):
    table = pd.read_excel(
        excel_path, sheet_name=sheetname)
    list_bm = []
    for i in range(1, 51):
        list_bm.append([i, (len(table[table.Position <= i].index)) / 22])
        # print(len(bm_v1_4_full[bm_v1_4_full.Position <= i].index))

    list_bm
    accuracy = pd.DataFrame(list_bm, columns=['Neighbors', 'Accuracy'])
    if write_csv:
        accuracy.to_csv('../accuracy.csv')

    return accuracy
