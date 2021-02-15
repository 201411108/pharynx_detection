import os
import natsort
import json
import math

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

    # if not os.path.isdir(self.RESULT_ROOT):
    #   os.mkdir(self.RESULT_ROOT)
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

      # if not os.path.isdir(self.RESULT_ROOT + czi_number):
      #   os.mkdir(self.RESULT_ROOT + czi_number)
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

  def create_dir(self):
    dir_creator = DirCreator()

    dir_creator.create_root_dir()
    dir_creator.create_czi_dir()
    dir_creator.create_image_dir()

class ResultWriter:

  def pythagoras_score(self, x, y, gt_x, gt_y):
    x_diff = int(math.pow(x - gt_x, 2))
    y_diff = int(math.pow(y - gt_y, 2))

    return math.sqrt(x_diff + y_diff)

  def write_txt(self, score_list, fname, sep=' '):
    """deprecated
    list를 받아 txt 파일을 생성하는 함수
      input : score_list - 대상 리스트, fname - 생성할 파일 이름, sep - 간격(default = ' ')
      output : 없음. txt 파일 생성됨
    """
    file = open(fname, 'w')
    vstr = ''

    for a in score_list:
      for b in a:
        vstr = vstr + str(b) + sep
      vstr = vstr.rstrip(sep)
      vstr = vstr + '\n'

    file.writelines(vstr)
    file.close()

  def write_json(self, score_data, result_file_name):
    """
    결과를 json 파일로 작성하는 함수
      input : score_data - 정보가 저장된 객체, result_file_name - 경로 + 해당 동물 이름을 갖고 있는 결과 파일 이름
      output : json 파일
    """
    result_file = result_file_name + '.json'

    with open(result_file, 'w', encoding='utf-8') as json_file:
      json.dump(score_data, json_file, ensure_ascii=False, indent='\t')

# if __name__ == '__main__':
#   dir_creator = DirCreator()

#   dir_creator.create_root_dir()
#   dir_creator.create_czi_dir()
#   dir_creator.create_image_dir()

  # data = {}
  # data['name'] = 'kim'
  # data['age'] = 26
  # data['favorite'] = ['sing', 'game']

  # rw = ResultWriter()
  # rw.write_json(data, 'test')