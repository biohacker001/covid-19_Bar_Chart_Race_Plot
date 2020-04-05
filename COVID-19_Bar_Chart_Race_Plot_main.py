# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:06:06 2020

@author: Lifeng Liu

code was adapted from https://towardsdatascience.com/bar-chart-race-in-python-with-matplotlib-8e687a5c8a41
"""



# import module
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import datetime



# read in date
df_original = pd.read_csv('C:/Users/Lifeng Liu/Desktop/bar_chart_race_python_project/total-cases-covid-19.csv', 
                 usecols=['Entity', 'Code', 'Date', 'Total confirmed cases of COVID-19 (cases)']) # date source: https://ourworldindata.org/coronavirus-data


df_country = pd.read_csv('C:/Users/Lifeng Liu/Desktop/bar_chart_race_python_project/countries_and_regions_flag_info_updated_local_image.csv',encoding='ISO-8859-1',
                         usecols=['Entity', 'region','Image URL']) # date source: https://app.flourish.studio/
# encoding setting is to avoid error message "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 18: invalid continuation byte". 

#df.head(4)
#df_country["Entity"].head(4)

df=pd.merge(df_original, df_country, on="Entity") # this merge removes country or regions without continent info or flag info.


#blob:https://ourworldindata.org/a8e7bd2b-02eb-4e1a-87c5-cbe38a88b0a8
# total-cases-covid-19.csv
#another format
# https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
# https://opendata.ecdc.europa.eu/covid19/casedistribution/csv


# data transformation

current_date = "Apr 4, 2020"
dff = (df[df['Date'].eq(current_date)]
       .sort_values(by='Total confirmed cases of COVID-19 (cases)', ascending=False)  
       .head(10)) #top 10 was listed
#dff

"""
# basic chart
fig, ax = plt.subplots(figsize=(15, 8))
ax.barh(dff['Entity'], dff['Total confirmed cases of COVID-19 (cases)'])
"""

# color and labels
colors = dict(zip(
    ['Asia', 'Europe', 'Africa', 'Americas',
     'Oceania'],
    ['#adb0ff','#f7bb5f' , '#90d595', '#e48381',
     '#aafbff'] #, , '#eafb50' '#ffb3ff'=> pink
))
group_lk = df.set_index('Entity')['region'].to_dict()

"""
# test with single image 
flag = df.set_index('Entity')['Image URL'].to_dict()

import matplotlib.image as mpimg # add flag onto the output image
#mpimg.imread(flag["China"])
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

fig, ax = plt.subplots(figsize=(15, 8))
dff = dff[::-1]   # flip values from top to bottom
# pass colors values to `color=`
ax.barh(dff['Entity'], dff['Total confirmed cases of COVID-19 (cases)'], color=[colors[group_lk[x]] for x in dff['Entity']]) 
# iterate over the values to plot labels and values (Tokyo, Asia, 38194.2)
for i, (value, name) in enumerate(zip(dff['Total confirmed cases of COVID-19 (cases)'], dff['Entity'])):
    #print(i, value, name) # output e.g. 0 277965 United States
    #ax.text(value, i,     mpimg.imread(flag[name]),  ha='right')  # China: name
    #ax.text(value, i-.25, group_lk[name],  ha='right')  # Asia: group name
    ax.text(value, i,     value,           ha='left')   # 100000: value

    # test with adding flag icon on bar
    #didn't work. 4/4/2020
    arr_lena = mpimg.imread(flag[name])
    imagebox = OffsetImage(arr_lena, zoom=0.1)
    ab = AnnotationBbox(imagebox, (value, i))
    ax.add_artist(ab)

# Add year right middle portion of canvas
ax.text(1, 0.4, current_date, transform=ax.transAxes, size=20, ha='right')

"""



# polish style

dir_loc = 'C:/Users/Lifeng Liu/Desktop/bar_chart_race_python_project/image/'

fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(date):
    dff = df[df['Date'].eq(date)].sort_values(by='Total confirmed cases of COVID-19 (cases)', ascending=True).tail(10)  
    
    df2 = df_original[(df_original["Entity"]=="World") & (df_original["Date"]==date)].set_index("Entity", drop = False) #get the world total cases #set_index: assigning Entity as an index column to pandas dataframe
    world_total=df2.loc["World","Total confirmed cases of COVID-19 (cases)"]    
    ax.clear()
    ax.barh(dff['Entity'], dff['Total confirmed cases of COVID-19 (cases)'], color=[colors[group_lk[x]] for x in dff['Entity']])
    dx = dff['Total confirmed cases of COVID-19 (cases)'].max() / 200
    for i, (value, name) in enumerate(zip(dff['Total confirmed cases of COVID-19 (cases)'], dff['Entity'])):
        #ax.text(value-dx, i,     name,           size=12, weight=600, ha='right', va='bottom')
        #ax.text(value-dx, i-.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=10, ha='left',  va='center')
    # ... polished styles
    ax.text(1, 0.3, date, transform=ax.transAxes, color='#999999', size=60, ha='right', weight=800)
    ax.text(1, 0.1, f"World Total: {world_total}", transform=ax.transAxes, color='#999999', size=40, ha='right', weight=500)        
    ax.text(0, 1.06, 'Confirmed cases', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    #ax.set_yticks([]) # remoce y labels
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0.1, 1.10, 'Top 10 countries with most confirmed COVID-19 cases',transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, f'by @Lifeng Liu; {datetime.date.today()}', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
    #plt.savefig(dir_loc+ date +".png")

   
draw_barchart(current_date)
datelist =df_original[(df_original["Entity"]=="China")]["Date"].values.tolist()

"""
# draw separate images 
for date in datelist:
    #draw_barchart(date)
"""


#Animate Race

fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_barchart,frames=datelist) 
animator.save(dir_loc+f"{current_date} top 10 countries with COVID-19 cases confirmed.mp4")
