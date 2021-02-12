from aicsimageio.readers.czi_reader import CziReader
import numpy as np
import cv2, os, natsort, argparse
from PIL import Image
import cv2

"""
Scene info : 0부터 동물 개수 - 1까지, 각 mapping된 동물 정보는 세부 데이터 폴더(data_details) 참고
  026, 027 : 0 ~ 26 -> 27
  028, 029, 030 : 0 ~ 24 -> 25
"""
class ImageExporter:
  def __init__(self, czi_file, saved_img_dir, saved_img_type):
    self.czi_file = czi_file
    self.saved_img_dir = saved_img_dir
    self.saved_img_type = saved_img_type

  def read_czi(self, czi_name, scene_info):
    img = CziReader(czi_name, S=scene_info)

    shape = img.shape
    time_info = shape[2]
    
    return img, time_info

  def export_png_from_czi(self):
    """czi 파일을 읽어 추출한 각 동물의 이미지를 저장"""
    czi_name = str(self.czi_file).split('/')[2]
    czi_name = czi_name.split('.')[0]
    czi_name = czi_name.split('-')[0]

    if czi_name == '026' or czi_name == '027':
      scene_info = 27
    else:
      scene_info = 25

    for i in range(scene_info):
      img, time_info = self.read_czi(self.czi_file, i)
      saved_dir_list = natsort.natsorted(os.listdir(self.saved_img_dir))

      for j in range(time_info):
        file_name = self.saved_img_dir + saved_dir_list[i] + '/' + saved_dir_list[i] + '_' + str(j + 1) + self.saved_img_type
        if not os.path.isfile(file_name):
          data = img.get_image_data('CZYX', S=0, T=j)
          data = np.reshape(data, (500, 92))
          data = Image.fromarray(data)
          data.save(file_name)
        else:
          print('file alread existed')
          break

        print(file_name, 'is done')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--czi_file', type=str, default='./raw_data/026-004.czi', help='czi file name we want to read')
  parser.add_argument('--saved_img_dir', type=str, default='./images/', help='dir name we want to save the images exported from czi file')
  parser.add_argument('--saved_img_type', type=str, default='.png', help='only .png is available')
  
  opt = parser.parse_args()

  CZI_FILE = opt.czi_file
  IMG_DIR = opt.saved_img_dir
  IMG_TYPE = opt.saved_img_type

  image_exporter = ImageExporter(CZI_FILE, IMG_DIR, IMG_TYPE)
  image_exporter.export_png_from_czi()