import os
import argparse
import natsort

# TODO ::
# raw_data, data_details, 각 동물 경로로부터 .pharynx.dat 파일을 읽어 YOLO v3 에서 사용할 수 있는 .txt 파일 작성(각 이미지에 대해)
# argparse를 활용하여 데이터 경로 지정
# labels 폴더에 저장, images와 같은 폴더 구조로 작성
# 라벨_클래스 이름, 대상의 중점 x좌표, 대상의 중점 y좌표, 바운딩 박스의 width, 바운딩 박스의 height

# 1. 중점 좌표 읽어오는 모듈 작성
# 2. 읽어온 중점 좌표와 width, height 정보를 저장하는 모듈 작성

DATA_WIDTH = 92
DATA_HEIGHT = 500

def make_label(label_dir, save_dir, width, height):
  """ 데이터 정보로부터 기관의 좌표를 읽는 함수
    입력 :
      label_dir : './raw_data/data_details/(czi 파일 번호)/'
      save_dir : './labels/(czi 파일 번호)/'
      width : 바운딩 박스 너비
      height : 바운딩 박스 높이
      
    출력 : (0, x / 92, y / 500, width / 92, height / height)
  """
  if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

  file_id = label_dir.split('/')[3]
  animals = natsort.natsorted([animal for animal in os.listdir(label_dir) if animal != '.DS_Store'])

  for animal in animals:
    idx = 1
    save_each_dir = save_dir + animal + '/'
    info_file = label_dir + animal + '/' + file_id + '.pharynx.dat'

    if not os.path.isfile(info_file):
      continue

    if not os.path.isdir(save_each_dir):
      os.mkdir(save_each_dir)

    with open(info_file) as file:
      positions = file.read().splitlines()

      for position in positions:
        label_file = open(save_each_dir + animal + '_' + str(idx) + '.txt', 'w')
        x = round(int(position.split('\t')[1]) / DATA_WIDTH, 6)
        y = round(int(position.split('\t')[2]) / DATA_HEIGHT, 6)
        w = round(width / DATA_WIDTH, 6)
        h = round(height / DATA_HEIGHT, 6)
        # print(int(position.split('\t')[1]), int(position.split('\t')[2]))
        data = '0 ' + '%0.6f' % x + ' ' + '%0.6f' % y + ' ' + '%0.6f' % w + ' ' + '%0.6f' % h + '\n'
        label_file.write(data)
        data = ''

        label_file.close()
        idx += 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--label_dir', type=str, default='./raw_data/data_details/', help='기관의 중점 좌표가 있는 폴더명 입력')
  parser.add_argument('--save_dir', type=str, default='./labels/', help='라벨 정보를 저장할 폴더')
  # parser.add_argument('--save_type', type=str, default='.txt', help='저장을 원하는 라벨 타입') # 다른 모델을 사용할 경우 확장성 고려
  parser.add_argument('--width', type=int, default=25, help='바운딩 박스 너비')
  parser.add_argument('--height', type=int, default=25, help='바운딩 박스 높이')

  opt = parser.parse_args()

  make_label(opt.label_dir, opt.save_dir, opt.width, opt.height)