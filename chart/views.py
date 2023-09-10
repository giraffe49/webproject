from django.shortcuts import render
from django.shortcuts import redirect

from .forms import UserProfileForm
from chart.models import T1
from chart.models import T2
from chart.models import SensorData

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objs as go
from collections import Counter
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import json


# Create your views here.
def index( request ):

	#讀取sql資料
	t1_list = T1.objects.all().values()
	t2_list = T2.objects.all().values()

	t1df = pd.DataFrame(T1.objects.all().values())
	t2df = pd.DataFrame(T2.objects.all().values())

	dftype = t1df['t_type']
	t1coun = Counter(t1df["t_type"])
	t2coun = Counter(t2df["t2_type"])

	t1df2 = pd.DataFrame.from_dict(t1coun,orient='index',columns=["Count"])
	t2df2 = pd.DataFrame.from_dict(t2coun,orient='index',columns=["Count"])

	t1df2count=t1df2['Count']
	t2df2count=t2df2['Count']
	#整合垃圾桶與回收桶的數量資料
	all_count = pd.concat([t1df2count, t2df2count])
	
	# 長條圖
	fig = plot([go.Bar(x = ['寶特瓶', '玻璃', '鐵鋁罐' , '紙類', '一般'],
            y = all_count),
            ],output_type='div')

	
	#滿溢程度
	fulldf = pd.DataFrame(SensorData.objects.all().values())
	f_num = fulldf.at[0, 'distance_value']
	f_numpre = round((f_num / 30) * 100, 2)
	# f_numpre = f_num/30*100
	a = 26
	a_numpre = round((a / 30) * 100, 2)
	b = 29
	b_numpre = round((b / 30) * 100, 2)
	c = 27
	c_numpre = round((c / 30) * 100, 2)
	d = 28
	d_numpre = round((d / 30) * 100, 2)

	return render( request, "index.html", locals())

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()  # 将数据保存到数据库
        return redirect('index')  # 重定向到成功页面
    else:
        form = UserProfileForm()

    return render(request, 'contact.html', {'form': form})