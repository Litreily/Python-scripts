# cfachina spider

Spider of data from http://www.cfachina.org/cfainfo/organbaseinfoServlet

## How to use

1. modified [Parameters](#parameters)
2. run `python spider.py`

## Dependencies libs

- `requests`
- `bs4` - `BeautifulSoup`

## Parameters

- `path`: directory to save the data, modified in `class Storage`
- `pageSize`(option): an argument of request, default `20`, can modified in `class SpiderThread: self.page_size`

## Tips

- If set `pageSize` to `1000`, it will grab only one page for each meachanism, so it should be more faster