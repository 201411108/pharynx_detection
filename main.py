# 만든 모듈들이 실행할 구문
# main.py에서 각 객체 생성 시 필요한 구문들 전달하는 방식으로 수정? -> 경로 정보, 특히, 모든 모듈에서 경로를 필요로 함. 일단 짜놓고 교수님꼐 질문?

from utils import DirCreator
from export_image import ImageExporter
from video_convertor import VideoConvertor

import os, natsort

def create_dir():
  dir_creator = DirCreator()

  dir_creator.create_root_dir()
  dir_creator.create_czi_dir()
  dir_creator.create_image_dir()

def export_image():
  image_exporter = ImageExporter()

  image_exporter.export_png_from_czi()

def converse_video():
  video_convertor = VideoConvertor()

  for i in range(len(video_convertor.path_in_root)):
    input_dir = video_convertor.path_in_root[i]
    output_dir = video_convertor.path_out_root[i]

    animals = natsort.natsorted(os.listdir(input_dir))

    for animal in animals:
      print(animal, 'translated started', '=' * 15)
      # 수정됨, 동영상 이름이 동물 번호이기 때문에 굳이 폴더로 만들 필요가 없었음, 수정 완료
      video_convertor.make_video_from_images(input_dir + animal + '/', output_dir + animal + '.mp4')
      # print(output_dir + animal + '.mp4')
      print(animal, 'translated finished', '=' * 14)

if __name__ == '__main__':
  # directory create
  create_dir()

  # export images from czi files
  export_image()

  # convert images into videos
  converse_video()