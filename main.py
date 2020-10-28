# 만든 모듈들이 실행할 구문
# main.py에서 각 객체 생성 시 필요한 구문들 전달하는 방식으로 수정? -> 경로 정보, 특히, 모든 모듈에서 경로를 필요로 함. 일단 짜놓고 교수님꼐 질문?

from utils import DirCreator
from export_image import ImageExporter
from video_convertor import VideoConvertor
from detection import Detector

if __name__ == '__main__':
  # directory create
  dir_creator = DirCreator()
  dir_creator.create_dir()

  # export images from czi files
  image_exporter = ImageExporter()
  image_exporter.export_image()

  # convert images into videos
  video_convertor = VideoConvertor()
  video_convertor.converse_video()

  # get results
  detector = Detector()
  detector.detection()