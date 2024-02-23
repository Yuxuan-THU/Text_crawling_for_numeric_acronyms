import urllib3
from bs4 import BeautifulSoup
from datetime import date, timedelta

url_1 = r'https://cn.govopendata.com/renminribao/'
def getnum(date):
    url=url_1+date
    head={
        'Cookie':'_ga=GA1.1.1547022082.1680452416; __gads=ID=44ef9a2b064fae84-220c3ab9ebdc00e1:T=1680452417:RT=1680452417:S=ALNI_Mbu2tOnhXIDeutz83OrbmgDPJsg7Q; __gpi=UID=00000beb6987c258:T=1680452417:RT=1680519699:S=ALNI_Mas0GibtjY0YBAc8Rb2mhbA1RzWwQ; _ga_7NESVRSV0K=GS1.1.1680519698.5.1.1680519766.60.0.0',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
        }
    http=urllib3.PoolManager()
    
    response=http.request('GET',url)
    html=""
    html=response.data.decode()
    soup=BeautifulSoup(html,"html.parser")
    cards = soup.find_all(class_="card")
    num=len(cards)
    return num


def getdata(date):
    head={
        'Cookie':'_ga=GA1.1.1547022082.1680452416; __gads=ID=44ef9a2b064fae84-220c3ab9ebdc00e1:T=1680452417:RT=1680452417:S=ALNI_Mbu2tOnhXIDeutz83OrbmgDPJsg7Q; __gpi=UID=00000beb6987c258:T=1680452417:RT=1680519699:S=ALNI_Mas0GibtjY0YBAc8Rb2mhbA1RzWwQ; _ga_7NESVRSV0K=GS1.1.1680519698.5.1.1680520226.52.0.0',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
        }
    num=getnum(date)
    for i in range(num):
        url_now=url_1+date+"/"+str(i+1)
        http=urllib3.PoolManager()
        response=http.request('GET',url_now)
        html=response.data.decode()
        soup=BeautifulSoup(html,"html.parser")
        cards = soup.find_all(class_="card")
        with open(date.replace("/", "")+".txt", "a") as f: # 注意这里改为追加模式"a"
            for card in cards:
                card_text = card.find("p", class_="card-text").text.strip()
                f.write(card_text + "\n\n") # 添加一个空行
                
#按时间线开爬
start_date = date(1946, 5, 15)
end_date = date(2003, 12, 31)
delta = timedelta(days=1)
while start_date <= end_date:
    #print(start_date.strftime("%Y/%m/%d"))
    date_now=start_date.strftime("%Y/%m/%d")
    getdata(date_now)
    print(date_now)
    start_date += delta