import cv2, os, sys, natsort, argparse
import numpy as np

class VideoConvertor:
  FPS = 50

  def __init__(self, input_img_dir, output_dir):
    self.input_img_dir = input_img_dir
    self.output_dir = output_dir

  def make_video_from_images(self, path_in_dir, path_out):
    """
    이미지를 비디오로 만들어주는 함수
      input : path_in_dir - 이미지가 저장되어 있는 폴더 경로, path_out - 출력 결과 경로 + 파일명
      output : path_out 지정한 파일명으로 영상 생성
    """
    output = path_out

    # 이미 생성한 경우 진행하지 않는다.
    if os.path.isfile(output):
      print('file already existed')
      # sys.exit()
      return
    else:
      frame_array = []
      files = [f for f in os.listdir(path_in_dir) if os.path.isfile(os.path.join(path_in_dir, f))]

      # file 이름순으로 정렬
      sorted_files = natsort.natsorted(files)

      # for f in sorted_files:
      #   print(f)

      count = 0
      total = len(sorted_files)

      for i in range(len(sorted_files)):
        # ignore .DS_Store for MacOS
        if sorted_files[i] == '.DS_Store':
          print('.DS_Store deleted')
          os.remove(path_in_dir + '.DS_Store')
        else:
          filename = path_in_dir + sorted_files[i]
          img = cv2.imread(filename)
          height, width, _ = img.shape # layers -> deprecated
          size = (width, height)

          frame_array.append(img)

          out = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'mp4v'), self.FPS, size)

          for i in range(len(frame_array)):
            out.write(frame_array[i])

          out.release()

          count += 1
          if count % 100 == 0 or count == total:
            print('Processing : ', count, ' / ', total)
    
    print(output, ' done')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_img_dir', type=str, default='./images/026/', help='directory contains images that we want to convert into video')
  parser.add_argument('--output_dir', type=str, default='./videos/026/', help='directory for saving converted videos')

  opt = parser.parse_args()

  IMAGE_DIR = opt.input_img_dir
  VIDEO_DIR = opt.output_dir

  videoConvertor = VideoConvertor(IMAGE_DIR, VIDEO_DIR)

  animals = natsort.natsorted(os.listdir(IMAGE_DIR))

  for animal in animals:
    print(animal, 'translated started', '=' * 15)
    # 수정됨, 동영상 이름이 동물 번호이기 때문에 굳이 폴더로 만들 필요가 없었음, 수정 완료
    videoConvertor.make_video_from_images(IMAGE_DIR + animal + '/', VIDEO_DIR + animal + '.mp4')
    # print(output_dir + animal + '.mp4')
    print(animal, 'translated finished', '=' * 14)