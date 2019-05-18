# -*- coding=utf-8 -*-
# fork from www.shiyanlou.com

from PIL import Image
import argparse

#命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output')   #输出文件

args = parser.parse_args()

IMG = args.file
OUTPUT = args.output

chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
def px2char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(chars)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return chars[int(gray/unit)]

if __name__ == '__main__':
    img = Image.open(IMG)
    width, height = img.size
    height = (int)(80 * height / width)
    width = 120
    img = img.resize((width,height), Image.NEAREST)

    txt = ""

    for i in range(height):
        for j in range(width):
            txt += px2char(*img.getpixel((j,i)))
        txt += '\n'

    print(txt)

    #字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)
