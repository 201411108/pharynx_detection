# 만든 모듈들이 실행할 구문
# main.py에서 각 객체 생성 시 필요한 구문들 전달하는 방식으로 수정?

from utils import DirCreator


if __name__ == '__main__':
  dir_creator = DirCreator()

  dir_creator.create_root_dir()
  dir_creator.create_czi_dir()
  dir_creator.create_image_dir()