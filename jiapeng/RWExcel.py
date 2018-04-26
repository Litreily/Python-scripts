# -*- coding: utf-8 -*-

import xlwt
import xlrd
from xlutils.copy import copy

from time import sleep


def write_row(table, row_index, row_value):
    for i in range(len(row_value)):
        table.write(row_index, i, row_value[i])


# get origial data from xls file
path = 'D:/litreily/Desktop/TC.xls'
# path = 'E:/Guangtao.Wu/Desktop/TC.xls'
rb = xlrd.open_workbook(path)
orig_table = rb.sheet_by_name("原始数据")

wb = copy(rb)

try:
    new_table = wb.get_sheet('新数据')
except Exception as e:
    new_table = wb.add_sheet('新数据')
finally:
    pass

# add table header
for i in range(4):
    new_table.write(0, i, ('产品名称', '类型', '日期', '金额')[i])

# initial data
index = 0  # 新表索引
pre_product = None  # 前个产品名称

# start processing
for row in range(1, orig_table.nrows):
    print('processing row %s ......' % row)
    row_value = orig_table.row_values(row)
    data_type = row_value[1]


    # 检测产品变更
    product_changed = (not pre_product) or (row_value[0] != pre_product)
    if product_changed:
        product_changed = False
        pre_product = row_value[0]
        cur_product_row = row

        pre_date = row_value[2]  # 当前产品初始日期

        share = 0.0  # 确认份额/赎回份额

        equity = 1.0  # 单位净值
        equity_saved = True  # 单位净值的保存标志

        pre_share_sum = 0.0
        pre_others_sum = 0.0
        share_sum = 0.0  # 确认份额，赎回份额累积求和
        others_sum = 0.0  # 除 '交易' 和 '回款' 外的原始数据总和


    # 检测日期变更
    date_changed = row_value[2] != pre_date
    if date_changed:
        pre_date = row_value[2]
        pre_share_sum = share_sum
        pre_others_sum = others_sum

        equity_saved = False


    # 依据数据类型计算和存储数据
    if '金' in data_type:
        share_name = '{0}份额-{1}'.format(
            {
                True : '确认',
                False: '赎回'
            }.get('入金' in data_type), data_type[-1])

        if (row - cur_product_row) < 2:
            share = row_value[3]
            share_sum += share
            others_sum += share

            write_row(new_table, index + 1, row_value)
            write_row(new_table, index + 2, [row_value[0], share_name, row_value[2], share])
            index += 2
            continue

        # 计算单位净值
        if not equity_saved:
            equity_saved = True
            equity = pre_others_sum / pre_share_sum
            write_row(new_table, index + 1, [row_value[0], '单位净值', row_value[2], equity])
            index += 1
        
        # 计算确认份额或赎回份额
        share = row_value[3] / equity

        write_row(new_table, index + 1, row_value)
        write_row(new_table, index + 2, [row_value[0], share_name, row_value[2], share])
        index += 2

        # 累积份额及others_sum
        share_sum += share
        others_sum += row_value[3]
        
    elif '交易' in data_type or '回款' in data_type:
        index += 1
        write_row(new_table, index, row_value)

    else:
        index += 1
        write_row(new_table, index, row_value)
        others_sum += row_value[3]


print('saving data to the %s ......' % path)
while True:
    try:
        wb.save(path)
        break
    except PermissionError as pe:
        print('error: %s, please close the file first' % pe.strerror)
        sleep(5)
    finally:
        pass
print('Done!')