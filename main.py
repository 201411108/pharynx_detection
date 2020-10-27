# 만든 모듈들이 실행할 구문
# main.py에서 각 객체 생성 시 필요한 구문들 전달하는 방식으로 수정? -> 경로 정보, 특히, 모든 모듈에서 경로를 필요로 함. 일단 짜놓고 교수님꼐 질문?

from utils import DirCreator
from export_image import ImageExporter

def create_dir():
  dir_creator = DirCreator()

  dir_creator.create_root_dir()
  dir_creator.create_czi_dir()
  dir_creator.create_image_dir()

def export_image():
  image_exporter = ImageExporter()

  image_exporter.export_png_from_czi()

if __name__ == '__main__':
  # directory create
  create_dir()

  export_image()