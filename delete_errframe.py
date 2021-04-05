import os, natsort, argparse
from tqdm import tqdm

# .errframe을 읽어서 해당하는 프레임 삭제
# .errframe 파일이 없는 경우 건너뛰어야 한다.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_no', type=str, default='026', help='에러 프레임을 제거할 czi 파일 번호')
    parser.add_argument('--img_dir', type=str, default='./images/', help='에러 프레임을 제거할 이미지가 저장된 루트 경로')
    parser.add_argument('--err_info', type=str, default='./raw_data/data_details/', help='에러 프레임 정보(.errframe)가 저장된 파일의 경로')

    opt = parser.parse_args()

    FILE_NO = opt.file_no
    IMG_DIR = opt.img_dir
    ERR_INFO = opt.err_info

    animals = natsort.natsorted(os.listdir(IMG_DIR + FILE_NO))
    count = 0
    for animal in animals:
        # TODO :: 출력 예쁘게 정리
        print('delete error frames from ' + FILE_NO + '-' + animal)
        # TODO :: utils로 제거
        if animal == '.DS_Store':
            continue

        # ./images/026/P01/
        images = natsort.natsorted(os.listdir(IMG_DIR + FILE_NO + '/' + animal + '/'))

        # ./raw_data/data_details/026/P01/026.errframe
        err_file = ERR_INFO + FILE_NO + '/' + animal + '/' + FILE_NO + '.errframe'
        if not os.path.isfile(err_file):
            continue

        with open(err_file) as file:
            err_frames = file.read().splitlines()

        for err_frame in tqdm(err_frames):
            if animal + '_' + err_frame + '.png' in images:
                # print(animal + '_' + err_frame + '.png', 'is deleted')
                os.remove(IMG_DIR + FILE_NO + '/' + animal + '/' + animal + '_' + err_frame + '.png')
                count += 1
        print(FILE_NO + '_' + animal + '\'s errframe :', len(err_frames))
                
    print('# of deleted error frames in ' + FILE_NO + ' : ' + str(count))