import os
import numpy as np
import psycopg2
from data.connect_postgres import get_postgresql_connection

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

#rootdir = '/Users/pauli/Documents/Studium/Master/4_Semester/TUM_DI_Lab/Data_Labeling/Testset'
#classlabels = get_test_paths(rootdir)
#classlabels[0]




def get_pipeline_accuracy(n, test_watermarks_paths):
    tests = len(test_watermarks_paths)

    drawing_found = np.zeros(tests)
    # Step 1 get image and nearest neighbors

    for image in test_watermarks_paths:

        get_nearest_neighbors_path




        


