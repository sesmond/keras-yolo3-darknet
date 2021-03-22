#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Title   :TODO
@File    :   data_convert.py    
@Author  : vincent
@Time    : 2021/3/21 下午12:34
@Version : 1.0 
"""
import os
import glob
import xml.etree.ElementTree as ET

from utils import file_utils


def xml_to_csv(path, output_path):
    xml_list = []
    file_utils.check_path(output_path)
    out_file = os.path.join(output_path, 'train.txt')
    f = open(out_file, 'w', encoding="utf-8")
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        line_list = []
        file_name = root.find('filename').text
        line_list.append(file_name)
        width = int(root.find('size')[0].text),
        height = int(root.find('size')[1].text)
        for member in root.findall('object'):
            class_id = member[0].text
            class_id = "0"
            x_min = member[4][0].text
            y_min = member[4][1].text
            x_max = member[4][2].text
            y_max = member[4][3].text
            box = [x_min, y_min, x_max, y_max, class_id]
            line_list.append(",".join(box))
        line_str = " ".join(line_list)
        f.write(line_str + "\n")
    f.close()
    return


def main():
    root_path = "../../dataset/raccoon_dataset"
    root_path = "../../dataset/cigarette"
    anno_path = os.path.join(root_path, 'annotations')
    output_path = "data"
    output_path = os.path.join(root_path, "data")
    xml_to_csv(anno_path, output_path)


if __name__ == '__main__':
    main()
