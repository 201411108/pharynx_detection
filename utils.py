import os
import natsort

class DirCreator:
  """프로그램 실행 결과를 저장하기 위한 디렉토리를 생성하는 class"""
  def __init__(self):
    self.IMAGE_ROOT = './images/'
    self.VIDEO_ROOT = './videos/'
    self.RESULT_ROOT = './results/'

    self.CZI_LISTS = ['026', '027' ,'028' ,'029' ,'030']

  def create_root_dir(self):
    """이미지, 동영상, 결과를 저장할 디렉토리를 만드는 함수
      입력 : none
      출력 : 이미지, 동영상, 결과를 저장할 최상위 디렉토리 생성
    """
    if not os.path.isdir(self.IMAGE_ROOT):
      os.mkdir(self.IMAGE_ROOT)
      # print('Image directory created')

    if not os.path.isdir(self.VIDEO_ROOT):
      os.mkdir(self.VIDEO_ROOT)
      # print('Video directory created')

    if not os.path.isdir(self.RESULT_ROOT):
      os.mkdir(self.RESULT_ROOT)
      # print('Result directory created')

  def create_czi_dir(self):
    """czi 파일(026, 027, 028, 029, 030)에 해당하는 디렉토리를 만드는 함수
      입력 : none,
      출력 : 이미지, 동영상, 결과 루트에 대해 czi 파일의 이름을 갖는 디렉토리 생성
    """
    for czi_number in self.CZI_LISTS:
      if not os.path.isdir(self.IMAGE_ROOT + czi_number):
        os.mkdir(self.IMAGE_ROOT + czi_number)
        # print(self.IMAGE_ROOT + czi_number, 'directory created')

      if not os.path.isdir(self.VIDEO_ROOT + czi_number):
        os.mkdir(self.VIDEO_ROOT + czi_number)
        # print(self.VIDEO_ROOT + czi_number, 'directory created')

      if not os.path.isdir(self.RESULT_ROOT + czi_number):
        os.mkdir(self.RESULT_ROOT + czi_number)
        # print(self.RESULT_ROOT + czi_number, 'directory created')

  def create_image_dir(self):
    """이미지 디렉토리/czi 디렉토리 내 포함되어 있는 동물의 디렉토리를 만드는 함수
      입력 : none
      출력 : ./image/# of czi 내에 해당하는 동물의 디렉토리 생성
    """
    root_czi_dir = './raw_data/data_details/'

    for czi_number in self.CZI_LISTS:
      animal_list = natsort.natsorted(os.listdir(root_czi_dir + czi_number + '/'))
      # print(animal_list)
      for animal in animal_list:
        dir_name = self.IMAGE_ROOT + czi_number + '/' + animal
        
        if not os.path.isdir(dir_name):
          os.mkdir(dir_name)
          print(dir_name, 'created')


# if __name__ == '__main__':
#   dir_creator = DirCreator()

#   dir_creator.create_root_dir()
#   dir_creator.create_czi_dir()
#   dir_creator.create_image_dir()