"""
video_tools_v2: just a cleaneup version of v1
"""
# a simple code to read video files
import pylab
import imageio
import os
import cv2 as cv
from tqdm import tqdm
# import json_to_xml
# import file_tools


def extract_frames(folder_name, filename=None, output_folder='', extract_step=1, extractor='imageio'):
    if filename is not None:
        fullpath = os.path.join(folder_name, filename)
    else:
        fullpath = folder_name
        filename = os.path.basename(fullpath)
        folder_name = os.path.dirname(folder_name)
    if extract_step == 1:
        print("Extracting all frames from {}".format(fullpath))
    else:
        print("Extracting each frame every {} frames from {}".format(extract_step, fullpath))
    if not output_folder:
        output_folder = '{}_frames{}'.format(filename.split('.')[0], extract_step)
    output_path = os.path.join(folder_name, output_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if extractor == 'imageio':
        vid = imageio.get_reader(fullpath, 'ffmpeg')

        # length = len(vid)->does not work anymore
        length = vid.get_meta_data()['duration']*vid.get_meta_data()['fps']
        print('Found {} frames.'.format(length))
        # extract all frames
        for i in tqdm(range(0, int(length/extract_step))):
            image = vid.get_data(i*extract_step)
            filename2 = '{}_{:05}.jpg'.format(filename.split('.')[0], i*extract_step)
            fullpath2 = os.path.join(folder_name, output_folder, filename2)
            # print(fullpath2)
            imageio.imwrite(fullpath2, image)
        print('{} frames were extracted'.format(int(length/extract_step)))

    elif extractor == 'opencv':
        i = 0
        j = 0
        num_frames = 0
        vid = cv.VideoCapture(fullpath)
        while True:
            ok, image = vid.read()
            if not ok:
                break
            if i % extract_step == 0:
                filename2 = '{}_{:05}.jpg'.format(filename.split('.')[0], j*extract_step)
                fullpath2 = os.path.join(folder_name, output_folder, filename2)
                cv.imwrite(fullpath2, image)
                num_frames += 1
                j += 1
            i += 1
            print(f'\nloading...{i}')
        print('\n\nTotal frames = {}.\nExtract step every {} frames.\nFinal frames were extracted = {}'.format(i,extract_step,num_frames))
    else:
        raise ValueError('Extractor was not recognised. Options are "imageio" and "opencv".')


def main():
    # extract all frames of a video to a folder
    # folder_name = '/home/gorfanidis/Datasets/Aresibo/Tekever/'
    # filename = 'video_20210908_142701.ts'  # 'VIRAT_S_040100_01_000347_000432.mp4' #'actions3.mpg'
    video_path = '/home/stayros/Desktop/video_01.mp4'
    extract_step =20
    extractor = 'opencv'  # 'imageio'  #
    extract_frames(video_path, extract_step=extract_step, extractor=extractor)

    # extract frames from all videos in folder
    # video_folder = '/home/gorfanidis/Datasets/7Shield/videos_in_winter_conditions/'
    # extract_step = 180
    # extractor = 'opencv'  # 'imageio'  #
    # video_list = file_tools.get_list_files(video_folder, pattern='*.mp4', relative=False)
    # for v in video_list:
    #     extract_frames(v, extract_step=extract_step, extractor=extractor)

    # parse all train videos from trecVid
    # extract_step = 1
    # json_path = r'D:\Call for Papers\TRECVID 2018\VIRAT-V1_JSON_validate_drop4_20180322/file-index.json' # 'D:/Call for Papers/TRECVID 2018/VIRAT-V1_JSON_train_drop4_20180322/file-index.json'
    # mpg_files = json_to_xml.extract_files_from_json(json_path)
    # base_folder = r'D:\Dataset\VIRAT dataset\VIRATv1\evaluation' # 'D:/Dataset/VIRAT dataset/VIRATv1'
    # for i, vid in enumerate(mpg_files):
    #     output_folder = '{}_frames{}'.format(vid.split('.')[0], extract_step)
    #     if os.path.exists(os.path.join(base_folder, vid)):
    #         if not os.path.exists(os.path.join(base_folder, output_folder)):
    #             extract_frames(base_folder, vid, output_folder=output_folder, extract_step=extract_step)
    #             i += 1
    #     else:
    #         print('Video file "{}" is missing'.format(os.path.join(base_folder, vid)))
    # print('Frames from {} videos were extracted'.format(i))


if __name__ == '__main__':
    main()
