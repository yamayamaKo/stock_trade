import requests
from bs4 import BeautifulSoup
import re 

# スクレイピング対象の URL にリクエストを送り HTML を取得する
res = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.text, 'html.parser')

a_tag = soup.find_all('a',{'class': 'external text'})
symbol = re.compile('[A-Z]+')
symbol_list = []
for item in a_tag:
    if re.fullmatch(symbol, item.get_text()):
        symbol_list.append(item.get_text())

print(len(symbol_list))
# for i in range(len(symbol_list)):
#     print(symbol_list[i])

# print(a_tag.decode_contents(formatter='html'))

# //*[@id="constituents"]/tbody/tr[1]/td[1]/a
# //*[@id="constituents"]/tbody/tr[2]/td[1]/a
# //*[@id="constituents"]/tbody/tr[505]/td[1]/a

# # title タグの文字列を取得する
# title_text = soup.find('title').get_text()
# print(title_text)
# # > Quotes to Scrape

# # ページに含まれるリンクを全て取得する
# links = [url.get('href') for url in soup.find_all('a')]
# print(links)

# # class が quote の div 要素を全て取得する
# quote_elms = soup.find_all('div', {'class': 'quote'})
# print(len(quote_elms))