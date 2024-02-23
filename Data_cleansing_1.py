import re
import pandas as pd
from datetime import date, timedelta
rule = r'[“‘]((?=[^“”‘’，]{1,8})(?=[^“”‘’，]*[零一二三四五六七八九十百千万亿两][^“”‘’，]*)[^“”‘’，·]{0,7}[零一二三四五六七八九十百千万亿两][^“”‘’，·]{0,7})[”’]'
pattern = '^[\u4e00-\u9fa5零一二两三四五六七八九十百千万亿]+$' #　排除只有数字
count_dict={}
def search_text(text,year,rule):
    year=str(year)
    if year not in count_dict:
        count_dict[year]={}
    matches = re.findall(rule, text) # 找文本中满足规则的所有文段
    for match in matches:
        if bool(re.match(pattern,match)):
            matches.remove(match)
    for match in matches:
        if match not in count_dict[year]:
            count_dict[year][match]=0
        count_dict[year][match]+=1

start_date = date(1979, 1, 1)
end_date = date(1980, 8, 7)
delta = timedelta(days=1)
dates=[]
while start_date <= end_date:
    #print(start_date.strftime("%Y/%m/%d"))
    date_now=start_date.strftime("%Y%m%d")
    dates.append(date_now)
    start_date += delta
    
count_dict={}
for date in dates:
    with open(str(date)+".txt",'r',encoding='gbk') as f:
        text_now=f.read()
    search_text(text_now,str(date)[:4],rule)
# print(count_dict)
# 将嵌套字典转换为DataFrame对象
df_dict = {}
for year, counts in count_dict.items():
    for phrase, phrase_count in counts.items():
        if phrase not in df_dict:
            df_dict[phrase] = {}
        df_dict[phrase][year] = phrase_count
print(df_dict)
df = pd.DataFrame(df_dict).transpose() # 横纵坐标转换
df.to_excel('result.xls',index=True)
