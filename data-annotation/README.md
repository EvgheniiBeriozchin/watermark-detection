# Data Annotation
To annotate our data, we are using [Label Studio](https://labelstud.io/).

## Installation
If you use or intend on using a Virtual Environment, do:
```python
python3 -m venv env # if you want to create a virtual environment
source env/bin/activate
```

Then: 
```
pip install label-studio
```

For an installation using homebrew, see [here](https://labelstud.io/guide/install.html#Install-using-Homebrew).

To test the program, run:
```
label-studio
```
Then open `localhost:8080/`in your browser to see the application. If this works, proceed to the setup.

## Setup
Before proceeding with the setup turn-off the application (Ctrl/Command + C in the Terminal).  
Make sure your Virtual Environment is on, if you use one.  

First enable saving/loading from local storage:
```
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=absolute-path-to-project-folder
```

Note here that the data (the images) need to be stored in a subfolder of `absolute-path-to-project-folder` so make sure that this path does not point to this Github repository as we don't want the data to land here.  

Note: the 2 lines above need to be run every time, before running the app.

Now, run the program:
```
label-studio
```
and go to `localhost:8080/`in your browser.

Press `Create` on the upper-right corner to create a new project. The Project Name does not matter. Ignore the Data Import Tab for now.  
In the `Labeling Setup` Tab, press `Custom Template` on the bottom-left. In the `Code` Tab, remove whatever code is present, and paste the text from `labeling-setup.txt`. Press `Save`.  

Go to the Settings Tab on the top right corner. Then select `Cloud Storage`.
  - Press Add Source Storage.
  - For Storage Type select `Local Files`.
  - For Absolute local path, write in the absolute path to your data folder. Note that this should be a child folder of the 
  `absolute-path-to-project-folder` you set up in the previous section. For example, if in the previous section you did:
  ```
  export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/mnt/d/watermark-project
  ```

  Then in `Absolute local path`, you can have something like: `/mnt/d/watermark-project/data`.
  Note2: It does not matter if the data folder has subfolders, even the ones that have meaning (like 'WZ-II...'). You can still select the generic data folder, as the subfolders will be preserved in the output annotation.

  To check that your path is valid, press `Check connection` at the bottom of the screen.

  - For File Filter Regex, write: `.*(jpe?g|png)`.
  - Select `Treat every bucket object as a source file`.
  - Press `Add Storage`.


Now press `Add Target Storage` and select `Local Files`.  
Because the output files are numbers that may collide between all annotators, we will be splitting the annotations into folders for each annotator. I am preparing a script to combine all annotations afterwards.  
Thus, in `Absolute local path` write in the absolute path to this repository and to your specific folder and press Add Storage. Something like:
```
/mnt/d/watermark-project/watermark-detection/data-annotation/batch-{}/
``` 
Note: If you add new data to your source folder or want the output files to be saved to the output folder, you have to come back to this tab and press `Sync Storage` for each of the storages.

As soon as you uploaded some data to the source storage and synced, you are ready to label data.  
Note: The data which each annotator has to annotate is written in the corresponding Excel file. The progress should also be marked there.

## Labeling
The labeling is mostly straightforward:
 - Select one of the 2 tags available (Drawing vs Watermark), now you can draw a bounding box around the corresponding instance. Make sure it's as tight as possible without losing any relevant strokes. You can modify your selecting by pressing and dragging, or double-pressing and resizing.
 - To make multiple annotations on the same image, press the Label again.
 - Then proceed to mark whatever Checkboxes apply and press Submit.
 - As soon as you are done with a labeling session, Sync the storage and push the outputs to Github.



