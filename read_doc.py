# -*- coding: utf-8 -*-
import os
import win32com.client
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

files = [f for f in os.listdir('.') if f.endswith('.doc')]
if files:
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(os.path.abspath(files[0]))

    tables = doc.Tables

    # 读取前50个表格
    results = []
    for i in range(1, min(51, tables.Count + 1)):
        try:
            table = tables(i)
            if table.Rows.Count > 0:
                # 尝试读取表格标题（通常第一行或第一列包含表名）
                # 先尝试第一行
                row1_cells = table.Rows(1).Cells
                if row1_cells.Count > 0:
                    cell1_text = row1_cells(1).Range.Text.strip()
                    # 移除\r和\x07
                    cell1_text = cell1_text.replace('\r', '').replace('\x07', '')
                    results.append('%d|%s' % (i, cell1_text))
        except Exception as e:
            results.append('%d|ERROR: %s' % (i, str(e)))

    # 写入文件
    with open('../table_list.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

    doc.Close()
    word.Quit()

    print('Done. Tables read: %d' % len(results))
