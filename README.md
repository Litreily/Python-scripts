# Python Demos

> some demos which coding with python

## cfachina spider

Spider of data from http://www.cfachina.org/cfainfo/organbaseinfoServlet

### How to use

1. modified [Parameters](#parameters)
2. run `python cfachina_spider.py`

### Dependencies libs

- `requests`
- `bs4` - `BeautifulSoup`
- `xlwt`, `xlrd`, `xlutils`

### Parameters

- `path`: directory to save the data, modified in `class Storage`
- `pageSize`(option): an argument of request, default `20`, can modified in `class SpiderThread: self.page_size`
- `filetype`(option): can be `.xls` or `.txt`, default is `.xls`

### Tips

- If set `pageSize` to `1000`, it will grab only one page for each meachanism, so it should be more faster
- Save to `.txt` file is more faster then `.xls` file

## RWExcel

Read and write data from .xls files

### Dependencies libs

- `xlwt`, `xlrd`, `xlutils`
