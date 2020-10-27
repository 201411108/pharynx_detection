from aicsimageio.readers.czi_reader import CziReader
import numpy as np
import cv2
import os
import natsort
from PIL import Image

"""
Scene info : 0부터 동물 개수 - 1까지, 각 mapping된 동물 정보는 세부 데이터 폴더(data_details) 참고
  026, 027 : 0 ~ 26 -> 27
  028, 029, 030 : 0 ~ 24 -> 25
"""
class ImageExporter:
  DIR_IMAGES = ['./images/026', './images/027', './images/028', './images/029', './images/030']
  IMAGES = ['./raw_data/026-004.czi', './raw_data/027-005.czi', './raw_data/028-003.czi', './raw_data/029-001.czi', './raw_data/030-002.czi']
  SCENE_INFO = [27, 25]

  def read_czi(self, image_name, scene_info):
    img = CziReader(image_name, S=scene_info)

    shape = img.shape
    time_info = shape[2]
    
    return img, time_info

  def export_png_from_czi(self):
    """czi 파일을 읽어 추출한 각 동물의 이미지를 저장"""
    for i in range(len(self.IMAGES)):
      # get scene_info
      # IMAGES : 0(026), 1(027) -> SCENE_INFO : 0
      # IMAGES : 2(028), 3(029), 4(030) -> SCENE_INFO : 1
      scene_info = 0

      if i < 4:
        scene_info = i // 2
      else:
        scene_info = 1

      root_dir = self.DIR_IMAGES[i]

      # read scene image
      for j in range(self.SCENE_INFO[scene_info]):
        img, time_info = self.read_czi(self.IMAGES[i], j)
        saved_dir_list = natsort.natsorted(os.listdir(root_dir))

        # print(saved_dir_list[j], " ", IMAGES[i], "'s scene info : ", j, ", time info : ", time_info)

        # export image
        for k in range(time_info):
          # this will be checked -> 이미 존재할 경우에는 생성하지 않아야 한다.
          file_name = root_dir + '/' + saved_dir_list[j] + '/' + saved_dir_list[j] + '_' + str(k + 1) + '.png'
          if not os.path.isfile(file_name):
            data = img.get_image_data("CZYX", S=0, T=k)
            data = np.reshape(data, (500, 92))
            data = Image.fromarray(data)
            data.save(root_dir + '/' + saved_dir_list[j] + '/' + saved_dir_list[j] + '_' + str(k + 1) + '.png')
          else:
            print('file already existed')
            break
          # print(root_dir + '/' + saved_dir_list[j] + '/' + saved_dir_list[j] + '_' + str(k + 1) + '.png done')

        print(root_dir + '/' + saved_dir_list[j] + ' export done')

# if __name__ == "__main__":
#   image_exporter = ImageExporter()
#   image_exporter.export_png_from_czi()