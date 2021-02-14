# pharynx_detection

## Requirements
* python 3.6.5 ++
* aicsimageio
* opencv-contrib-python

### install requirements
  ```
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

## Module informations
1. utils.py
  * DirCreator : Class that generates a path to save the results of a program's execution
2. export_image.py
  * ImageExporter : Class for exporting images corresponding to each animal from the czi file
3. video_convertor.py
  * VideoConvertor : Class that converts the extracted image into a moving image corresponding to each animal in the czi file

## How to run code
1. make directory name `raw_data`
2. put czi files in `raw_data`
3. put data details in `raw_data/data_details`
4. `python main.py`
