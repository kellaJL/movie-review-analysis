from wordcloud import WordCloud,STOPWORDS
import pandas as pd 
import jieba
import matplotlib.pyplot as plt 
#import seaborn as sns
from pyecharts import Geo,Style,Line,Bar,Overlap,Page  #Geo地理坐标系   Style   Line折线/面积图   Bar柱状图/条形图

page=Page()
f = open('movie_new.txt',encoding='utf-8')
data = pd.read_csv(f,sep=',',header=None,encoding='utf-8',names=['date','nickname','city','rate','comment'])

city = data.groupby(['city'])
rate_group = city['rate']

city_com = city['rate'].agg(['mean','count'])
##print(city_com)
city_com.reset_index(inplace=True)#重新设置索引index
city_com['mean'] = round(city_com['mean'],2)

#热力图分析
data_map = [(city_com['city'][i],city_com['count'][i]) for i in range(0,city_com.shape[0])]
#print(data_map)
style = Style(title_color="#fff",title_pos = "center",
            width = 1200,height = 600,background_color = "#404a59")

geo = Geo("电影粉丝人群地理位置","数据来源：猫眼电影",**style.init_style)

while True:
    try:
        attr,val = geo.cast(data_map)
       # geo.add("",attr,val,visual_range=[0,20],visual_text_color="#fff",symbol_size=20,is_visualmap=True,is_piecewise=True, visual_split_number=4)
        geo.add("", attr, val, type="heatmap",visual_range=[0,20], visual_text_color="#fff", symbol_size=15, is_visualmap=True,is_piecewise=True)

    except ValueError as e:
        e = str(e)
        e = e.split("No coordinate is specified for ")[1]#获取不支持的城市名
        for i in range(0,len(data_map)):
            if e in data_map[i]:
                data_map.pop(i)
                break
        continue
    else:
        break
#geo.render('fans_locations.html')
page.add(geo)
#折线+柱图分析
city_main = city_com.sort_values('count',ascending=False)[0:20]
#print(city_main)
attr = city_main['city']
v1 = city_main['count']
v2 = city_main['mean']
#print(attr,v1,v2)
line = Line("主要城市评分")
line.add("城市",attr,v2,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
    mark_point=['min','max'],xaxis_interval=0,line_color='lightblue',
    line_width=4,mark_point_textcolor='black',mark_point_color='lightblue',
    is_splitline_show=False)
page.add(line)

bar = Bar("主要城市评论数")
bar.add("城市",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
    xaxis_interval=0,is_splitline_show=False)
page.add(bar)

overlap = Overlap()
overlap.add(bar)
overlap.add(line,yaxis_index=1,is_add_yaxis=True)
#overlap.render('主要城市评论数_平均分.html')
page.add(overlap)
page.render("movie_analysis.html")

#词云分析
#分词
comment = jieba.cut(str(data['comment']),cut_all=False)
wl_space_split = " ".join(comment)

#导入背景图
backgroud_Image = plt.imread('C_73.png') 
stopwords = STOPWORDS.copy()
#print("STOPWORDS.copy()",help(STOPWORDS.copy()))


wc = WordCloud(width=1024,height=768,background_color='white',
    mask=backgroud_Image,font_path="C:\simhei.ttf",
    stopwords=stopwords,max_font_size=400,
    random_state=50)

wc.generate_from_text(wl_space_split)
plt.imshow(wc)
plt.axis('off')#不显示坐标轴  
#plt.show()
wc.to_file(r'ciyun.jpg')