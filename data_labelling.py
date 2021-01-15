import os
import argparse

# TODO ::
# raw_data, data_details, 각 동물 경로로부터 .pharynx.dat 파일을 읽어 YOLO v3 에서 사용할 수 있는 .txt 파일 작성(각 이미지에 대해)
# argparse를 활용하여 데이터 경로 지정
# labels 폴더에 저장, images와 같은 폴더 구조로 작성
# 라벨_클래스 이름, 대상의 중점 x좌표, 대상의 중점 y좌표, 바운딩 박스의 width, 바운딩 박스의 height

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--label_dir', type=str, default='./raw_data/data_details/', help='기관의 중점 좌표가 있는 폴더명 입력')
  parser.add_argument('--save_dir', type=str, default='./labels/', help='라벨 정보를 저장할 폴더')
  # parser.add_argument('--save_type', type=str, default='.txt', help='저장을 원하는 라벨 타입') # 다른 모델을 사용할 경우 확장성 고려

  opt = parser.parse_args()