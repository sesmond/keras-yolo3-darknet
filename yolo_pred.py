import os
import sys
import argparse

from utils import file_utils
from yolo import YOLO, detect_video
from PIL import Image


def show(img, title='无标题'):
    '''
    本地测试时展示图片
    @param img:
    @param title:
    @return:
    '''
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.show()


def detect_img(yolo):
    cnt = 0
    while True:
        if cnt > 3:
            break
        cnt += 1
        img_p = input('Input image path:')
        files = file_utils.get_files(img_p)
        print("路径：", img_p, "中图片数量：", len(files))
        output_path = input('output image path:')
        for fp in files:
            print("预测图片：", fp)
            image = Image.open(fp)
            r_image = yolo.detect_image(image)
            base_name = os.path.basename(fp)
            r_image.save(os.path.join(output_path, base_name))
            is_continue = input("是否继续：y/n")
            if is_continue == 'n':
                break
    yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )
    # --anchors_path model_data/tiny_yolo_anchors.txt

    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )
    # --classes_path model_data/jd_classes.txt

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='./path2your_video',
        help="Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help="[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
