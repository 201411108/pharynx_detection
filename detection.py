import cv2
import sys
import os
import natsort
from utils import ResultWriter

class Detector:
  VIDEO_DIR = ['./videos/026/', './videos/027/', './videos/028/', './videos/029/', './videos/030/']
  BBOX_DIR = ['./raw_data/data_details/026/', './raw_data/data_details/027/', './raw_data/data_details/028/', './raw_data/data_details/029/', './raw_data/data_details/030/']
  SCORE_DIR = ['./results/026/', './results/027/', './results/028/', './results/029/', './results/030/']

  resultWriter = ResultWriter()

  def requirements_check(self):
    """
    goturn에 필요한 2가지 파일이 있는지 확인하는 함수
    """
    if not(os.path.isfile('./goturn.caffemodel') and os.path.isfile('./goturn.prototxt')):
      errorMsg = '''
        Could not find GOTURN model in current directory.
        Please ensure goturn.caffemodel and goturn,portotxt are in the current directory
      '''

      print(errorMsg)
      sys.exit()

  def load_video(self, video_path):
    """
    goturn을 실행하기 위한 video를 불러오기 위한 함수
      input : 확인하고자 하는 video path
      output : video 객체
    """
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
      print("Could not open video")
      sys.exit()

    return video

  def load_bbox(self, bbox_path):
    """
    data_details로 부터 각 동물의 기관의 최초 좌표를 읽어 반환하는 함수
      input : bbox_path - 각 동물의 기관 좌표가 적혀 있는 파일(.dat)
      output : 모든 좌표 정보, 최초 좌표
    """
    with open(bbox_path) as file:
      positions = file.read().splitlines()
      gt_bbox_positions = []
      for position in positions:
        gt_bbox_positions.append([int(position.split('\t')[1]), int(position.split('\t')[2])])

      initial_x = int(gt_bbox_positions[0][0])
      initial_y = int(gt_bbox_positions[0][1])
      # print(x, y)

    return gt_bbox_positions, initial_x, initial_y

  def goturn(self, video, gt_bbox, initial_x, initial_y):
    """
    goturn 라이브러리 실행 함수
      영상으로 보기를 원할 경우 주석처리 되어 있는 cv2 부분을 해제하면 된다.
      input : video 객체, bbox 최초 좌표
      output : frame 별 tracker가 추적한 x, y좌표, gt의 x, y좌표, 피타고라스 거리가 담긴 객체
    """
    tracker = cv2.TrackerGOTURN_create()

    ok, frame = video.read()

    if not ok:
      print('Cannot read video file')
      sys.exit()

    bbox = (initial_x, initial_y, 5, 5)

    ok = tracker.init(frame, bbox)

    # for pythagoras score, gt_list & frame num
    gt_bbox = gt_bbox
    frame_num = 1

    # score_object -> for saving results
    score_object = {}
    avg_score = 0

    while True:
      ok, frame = video.read()
      if not ok:
        break

      # timer = cv2.getTickCount()
      # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

      # bbox updated
      ok, bbox = tracker.update(frame)

      frame_object = {}
      flag = True

      if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

        # get pythagoras score
        # position boundary : 0 <= x <= 92, 0 <= y <= 500
        # 너무 말도 안되게 벗어나는 경우에는 실행을 중단하도록 만들 것
        # score 100 이상일 때, y좌표에서 100 이상 차이, x좌표 차이는 크지 않다.
        middle_p_x = (p2[0] + p1[0]) // 2 if (p2[0] + p1[0]) // 2 <= 92 else 92
        middle_p_y = (p2[1] + p1[1]) // 2 if (p2[1] + p1[1]) // 2 <= 500 else 500
        gt_x = gt_bbox[frame_num][0]
        gt_y = gt_bbox[frame_num][1]

        diff = middle_p_y - gt_y if middle_p_y - gt_y > 0 else -(middle_p_y - gt_y)

        if diff < 100: # 실행
          score = self.resultWriter.pythagoras_score(middle_p_x, middle_p_y, gt_x, gt_y)
          avg_score += score

          frame_object = {
            'tracking' : {
              'x' : middle_p_x,
              'y' : middle_p_y
            },
            'gt': {
              'x' : gt_x,
              'y' : gt_y
            },
            'score': score
          }

          score_object[frame_num] = frame_object
          # score_list.append([frame_num, score])
          print(frame_num, ':', middle_p_x, middle_p_y, gt_x, gt_y, '-> score :', score)
          # print(score)
          frame_num += 1
          # cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else: # 중단
          score_object = {}
          score_object['fail'] = 'from ' + str(frame_num) + ' tracking fail'
          flag = False
          break
      else:
        # cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        print('not ok')

      # cv2.putText(frame, "GOTURN Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

      # cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

      # cv2.imshow("Tracking", frame)

      # k = cv2.waitKey(1) & 0xff
      # if k == 27:
      #   break

    if flag:
      avg_score = avg_score / frame_num
      score_object['avg_score'] = avg_score
    # avg_score = avg_score / len(score_list)
    # print('avg_score :', avg_score)
    # score_list.append(['avg_score', avg_score])

    return score_object

  def detection(self):
    self.requirements_check()

    # load video & bbox_info
    for i in range(len(self.VIDEO_DIR)):
      videos = natsort.natsorted(os.listdir(self.VIDEO_DIR[i]))

      for video in videos:
        # bbox setting
        animal_num = video.split('.')[0]
        # czi_info = BBOX_DIR[i].split('/')[2]
        bbox_whole = natsort.natsorted(os.listdir(self.BBOX_DIR[i] + animal_num + '/'))
        bbox_dat = [f for f in bbox_whole if f.endswith('.pharynx.dat')]
        bbox = ''

        # for result saving
        result_file = self.SCORE_DIR[i] + animal_num

        # no .dat file existed
        if len(bbox_dat) == 0:
          continue
        else:
          bbox = self.BBOX_DIR[i] + animal_num + '/' + bbox_dat[0]

        # ignore .DS_Store for MacOS
        if video == '.DS_Store':
          print('.DS_Store deleted')
          os.remove(self.VIDEO_DIR[i] + '.DS_Store')
        # elif video == 'P16.mp4' and VIDEO_DIR[i] == './videos/026/':
        #   continue
        else:
          print(self.VIDEO_DIR[i], animal_num, 'file started', '=' * 15)
          video = self.load_video(self.VIDEO_DIR[i] + video)
          gt_bbox_info, initial_x, initial_y = self.load_bbox(bbox)
          # print(gt_bbox_info)
          # print(initial_x, initial_y)

          if not os.path.isfile(result_file + '.json'):
            scores = self.goturn(video, gt_bbox_info, initial_x, initial_y)
            self.resultWriter.write_json(scores, result_file)
            # resultWriter.write_txt(scores, result_file)

          print(self.VIDEO_DIR[i], animal_num, 'file finished', '=' * 14)

"""
if __name__ == '__main__':
  # make_result_dir()
  requirements_check()

  # load video & bbox_info
  for i in range(len(VIDEO_DIR)):
    videos = natsort.natsorted(os.listdir(VIDEO_DIR[i]))

    for video in videos:
      # bbox setting
      animal_num = video.split('.')[0]
      czi_info = BBOX_DIR[i].split('/')[2]
      bbox_whole = natsort.natsorted(os.listdir(BBOX_DIR[i] + animal_num + '/'))
      bbox_dat = [f for f in bbox_whole if f.endswith('.pharynx.dat')]
      bbox = ''

      # for result saving
      result_file = SCORE_DIR[i] + animal_num

      # no .dat file existed
      if len(bbox_dat) == 0:
        continue
      else:
        bbox = BBOX_DIR[i] + animal_num + '/' + bbox_dat[0]

      # ignore .DS_Store for MacOS
      if video == '.DS_Store':
        print('.DS_Store deleted')
        os.remove(VIDEO_DIR[i] + '.DS_Store')
      # elif video == 'P16.mp4' and VIDEO_DIR[i] == './videos/026/':
      #   continue
      else:
        print(VIDEO_DIR[i], animal_num, 'file started', '=' * 15)
        video = load_video(VIDEO_DIR[i] + video)
        gt_bbox_info, initial_x, initial_y = load_bbox(bbox)
        # print(gt_bbox_info)
        # print(initial_x, initial_y)

        if not os.path.isfile(result_file + '.json'):
          scores = goturn(video, gt_bbox_info, initial_x, initial_y)
          resultWriter.write_json(scores, result_file)
          # resultWriter.write_txt(scores, result_file)

        print(VIDEO_DIR[i], animal_num, 'file finished', '=' * 14)
"""