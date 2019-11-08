# -*- coding:utf-8 -*-
"""对格式一致的多个xls文件数据进行汇总，并写入一个新的xls文件
@date: 20190105
说明: 本程序最后得到的汇总文件中仅仅包含数据，并未添加表头及其它描述信息。所以，可以将所
得文件数据复制进一个带有表头信息的文件中，将数据部分替换即可。当然也可以改进程序，先复制
一个xls文件，之后进行更改，但记得需要使用到xlutils库的copy.copy函数
"""

import xlwt
from xlrd import open_workbook
# from xlutils.copy import copy

import os

# xls文件路径及汇总文件名
FILE_DIR = 'E:/litreily/文档/excel'
GATHER_FILE = '配置计划表2019年度新-汇总.xls'
GATHER_FILE_PATH = FILE_DIR + '/' + GATHER_FILE

# 配置表数据区域的起始位置和行列数
CONFIG_DATA_START_ROW = 6
CONFIG_DATA_START_COL = 2
CONFIG_DATA_ROWS = 35
CONFIG_DATA_COLS = 10

# 部分基本信息表数据区域的起始位置和行列数
BASICINFO_DATA_START_ROW = 7
BASICINFO_DATA_START_COL = 2
BASICINFO_DATA_ROWS = 10
BASICINFO_DATA_COLS = 2


def gather_from_single_file(filename, config_data, basicinfo_data):
    """从xls文件中读取配置表、部分基本信息表数据，并进行累加"""
    rb = open_workbook(filename)
    config_table = rb.sheet_by_index(1)
    basicinfo_table = rb.sheet_by_index(2)

    print('Dealing with file: ' + filename)

    for i in range(CONFIG_DATA_ROWS):
        ROW = CONFIG_DATA_START_ROW + i
        for j in range(CONFIG_DATA_COLS):
            COL = CONFIG_DATA_START_COL + j
            raw_value = config_table.cell(ROW, COL).value
            if '─' in str(raw_value):
                config_data[i][j] = '────'
            else:
                config_data[i][j] += int(raw_value)

    for i in range(BASICINFO_DATA_ROWS):
        ROW = BASICINFO_DATA_START_ROW + i
        for j in range(BASICINFO_DATA_COLS):
            COL = BASICINFO_DATA_START_COL + j
            raw_value = basicinfo_table.cell(ROW, COL).value
            if not raw_value:
                basicinfo_data[i][j] = ''
            elif '─' in str(raw_value):
                basicinfo_data[i][j] = '─'
            else:
                basicinfo_data[i][j] += int(raw_value)

    rb.release_resources()
    return config_data, basicinfo_data

def write_data_to_gather_file(filename, config_data, basicinfo_data):
    """将累加后的数据写入新的xls文件"""
    wb = xlwt.Workbook(encoding='utf-8')
    wb.add_sheet('封面')
    ws_config = wb.add_sheet('配置表')
    ws_basicinfo = wb.add_sheet('部门基本信息表')

    for i in range(len(config_data)):
        for j in range(len(config_data[0])):
            ws_config.write(i + CONFIG_DATA_START_ROW, j + CONFIG_DATA_START_COL,
                config_data[i][j])

    for i in range(len(basicinfo_data)):
        for j in range(len(basicinfo_data[0])):
            ws_basicinfo.write(i + BASICINFO_DATA_START_ROW, j + BASICINFO_DATA_START_COL,
                basicinfo_data[i][j])

    wb.save(filename)


def main():
    if not os.path.isdir(FILE_DIR):
        return

    # 删除已有的汇总文件
    if os.path.exists(GATHER_FILE_PATH):
        os.remove(GATHER_FILE_PATH)

    files = os.listdir(FILE_DIR)
    if not files:
        return

    config_data = [[0 for i in range(CONFIG_DATA_COLS)] for i in range(CONFIG_DATA_ROWS)]
    basicinfo_data = [[0 for i in range(BASICINFO_DATA_COLS)] for i in range(BASICINFO_DATA_ROWS)]

    for xls_file in files:
        config_data, basicinfo_data = gather_from_single_file(FILE_DIR + '/' + xls_file,
            config_data, basicinfo_data)

    # 将累加后的数据写入新文件
    print('\n配置表汇总数据：')
    print(*config_data, sep='\n')
    print('\n部分基本信息表汇总数据：')
    print(*basicinfo_data, sep='\n')
    write_data_to_gather_file(GATHER_FILE_PATH, config_data, basicinfo_data)
    print('\n汇总数据已存入文件：' + GATHER_FILE_PATH)

if __name__ == "__main__":
    main()
