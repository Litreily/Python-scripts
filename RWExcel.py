# -*- coding: utf-8 -*-

import xlwt
import xlrd
from xlutils.copy import copy


def write_row(table, row_index, row_value):
    print(row_value)
    for i in range(len(row_value)):
        table.write(row_index, i, row_value[i])


# get origial data from xls file
path = 'E:/Guangtao.Wu/Desktop/TC.xls'
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
share = 0.0  # 确认份额/赎回份额
equity = 1.0  # 单位净值
share_sum = 0.0  # 确认份额，赎回份额累积求和
others_sum = 0.0  # 除 '交易' 和 '回款' 外的原始数据总和

index = 0  # 新表索引

# start processing
for row in range(1, orig_table.nrows):
    row_value = orig_table.row_values(row)
    data_type = row_value[1]

    if '金' in data_type:
        share_name = '{0}份额-{1}'.format(
            {
                True : '确认',
                False: '赎回'
            }.get('入金' in data_type), data_type[-1])

        if row < 3:
            share = row_value[3]
            share_sum += share

            write_row(new_table, index + 1, row_value)
            write_row(new_table, index + 2, [row_value[0], share_name, row_value[2], share])
            index += 2
            continue

        # 计算单位净值
        equity = others_sum / share_sum
        # 计算确认份额或赎回份额
        share = row_value[3] / equity

        others_sum += row_value[3]
        share_sum += share

        # 存储数据
        write_row(new_table, index + 1, [row_value[0], '单位净值', row_value[2], equity])
        write_row(new_table, index + 2, row_value)
        write_row(new_table, index + 3, [row_value[0], share_name, row_value[2], share])
        index += 3

    elif '交易' in data_type or '回款' in data_type:
        index += 1
        write_row(new_table, index, row_value)
    else:
        index += 1
        write_row(new_table, index, row_value)
        others_sum += row_value[3]

wb.save(path)
