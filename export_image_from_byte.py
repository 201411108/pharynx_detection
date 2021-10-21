import numpy as np
import cv2, argparse, os, natsort
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--czi_file', type=str, default='./raw_data/028-003.czi', help='읽어올 czi 파일')
    parser.add_argument('--file_no', type=str, default='028', help='확인할 파일 번호, 읽어올 czi 파일과 동일한 번호 입력')
    parser.add_argument('--czi_pos', type=str, default='./raw_data/data_details/', help='바이트 위치 파일(.czipos)이 저장된 루트 경로')
    parser.add_argument('--save_dir', type=str, default='./images/', help='추출한 이미지를 저장할 경로')

    opt = parser.parse_args()

    CZI_FILE = opt.czi_file
    FILE_NO = opt.file_no
    CZI_POS = opt.czi_pos
    SAVE_DIR = opt.save_dir

    animals = natsort.natsorted(os.listdir(CZI_POS + FILE_NO))

    for animal in animals:
        print('export images from ' + FILE_NO + '-' + animal)
        # .DS_Store 제거
        # TODO :: utils로 빼기
        if animal == '.DS_Store':
            # os.remove(animal)
            print('skip the .DS_Store')
            continue

        # ./raw_data/data_details/028/P01/028.czipos
        with open(CZI_POS + FILE_NO + '/' + animal + '/' + FILE_NO + '.czipos') as f:
            czi_pos = f.read().splitlines()[3:]
            # print(czi_pos[3:])

            for frame in tqdm(range(len(czi_pos))):
                with open(CZI_FILE, 'rb') as ff: # 'rb' : read byte
                    ff.seek(int(czi_pos[frame]), 1)  # 첫 번째 프레임으로부터 몇 번째 바이트를 볼 것인지
                    data = ff.read(92000) # 크기가 92000

                encoded_data = np.fromstring(data, dtype=np.uint16) # dtype을 맞춰주지 않으면 이상한 결과가 나온다.
                encoded_data.resize((500, 92))

                # 필요한 경로 만들기
                # TODO :: utils로 정리
                if not os.path.isdir(SAVE_DIR):
                    os.mkdir(SAVE_DIR)

                if not os.path.isdir(SAVE_DIR + FILE_NO):
                    os.mkdir(SAVE_DIR + FILE_NO)

                if not os.path.isdir(SAVE_DIR + FILE_NO + '/' + animal):
                    os.mkdir(SAVE_DIR + FILE_NO + '/' + animal)

                # ./bImages/028/P01/P01_1.png
                cv2.imwrite(SAVE_DIR + FILE_NO + '/' + animal + '/' + animal + '_' + str(frame + 1) + '.png', encoded_data)
                frame += 1
