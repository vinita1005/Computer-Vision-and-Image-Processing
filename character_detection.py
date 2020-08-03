"""
Character Detection

The goal of this task is to experiment with template matching techniques. Specifically, the task is to find ALL of
the coordinates where a specific character appears using template matching.

There are 3 sub tasks:
1. Detect character 'a'.
2. Detect character 'b'.
3. Detect character 'c'.

You need to customize your own templates. The templates containing character 'a', 'b' and 'c' should be named as
'a.jpg', 'b.jpg', 'c.jpg' and stored in './data/' folder.

Please complete all the functions that are labelled with '# TODO'. Whem implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in utils.py
and the functions you implement in task1.py are of great help.

Do NOT modify the code provided.
Do NOT use any API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import any library (function, module, etc.).
"""


import argparse
import json
import os

import utils
from task1 import *   # you could modify this line


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img_path", type=str, default="./data/characters.jpg",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--template_path", type=str, default="",
        choices=["./data/a.jpg", "./data/b.jpg", "./data/c.jpg"],
        help="path to the template image")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./results/",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args


def detect(img, template):
    """Detect a given character, i.e., the character in the template image.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        coordinates: list (tuple), a list whose elements are coordinates where the character appears.
            format of the tuple: (x (int), y (int)), x and y are integers.
            x: row that the character appears (starts from 0).
            y: column that the character appears (starts from 0).
    """
    temp_len_x = len(template)
    temp_len_y = len(template[0])
    img_len_x = len(img)
    img_len_y = len(img[0])
    
    # NCC equation implemented as stated in the Szeliski book
    coordinates = []
   
    img_mean = find_mean(img)
    temp_mean = find_mean(template)
   
    img_mean_list = [ [ img_mean for i in range(img_len_y) ] for j in range(img_len_x) ]
    temp_mean_list = [ [ temp_mean for i in range(temp_len_y) ] for j in range(temp_len_x) ]
   
    I0 = template - temp_mean
    
    I0_sq =  [[y**2 for y in x] for x in I0]
   
    I0_sq_sum = 0
    for q in range(len(I0_sq)):
        I0_sq_sum = I0_sq_sum + sum(I0_sq[q])
    maximus = 0
    for m in range(len(img)):
        for n in range(len(img[0])):
            if m+temp_len_x < img_len_x and n+temp_len_y < img_len_y:
                numerator = 0
                denominator = 0
                encc = 0
                I1_sq_sum = 0
                numerator = 0
                sublist = [[]]
                sublist = utils.crop(img, m, m+temp_len_x, n, n+temp_len_y)

                I1 = sublist - img_mean
                I0_mul_I1 = utils.elementwise_mul(I0,I1)
                for o in range(len(I0_mul_I1)):
                    numerator = numerator + sum(I0_mul_I1[o])
                
                I1_sq = [[y**2 for y in x] for x in I1]

                for p in range(len(I1_sq)):
                    I1_sq_sum = I1_sq_sum + sum(I1_sq[p])

                denominator = (I0_sq_sum ** 0.5) * (I1_sq_sum ** 0.5)
                if denominator!=0:
                    encc = numerator/denominator
                    if encc>0.82:
                        coordinates.append([m,n])
    
    #raise NotImplementedError
    return coordinates

def find_mean(img):
    img_sum = 0
    for t in range(len(img)):
        img_sum = img_sum + sum(img[t])
    n = len(img)*len(img[0])
    img_mean = img_sum/n
    return img_mean

def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()

    img = read_image(args.img_path)
    template = read_image(args.template_path)

    coordinates = detect(img, template)

    template_name = "{}.json".format(os.path.splitext(os.path.split(args.template_path)[1])[0])
    save_results(coordinates, template, template_name, args.rs_directory)


if __name__ == "__main__":
    main()
