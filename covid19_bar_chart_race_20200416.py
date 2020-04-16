# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:03:32 2020

@author: Lifeng Liu
"""

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as img
import matplotlib.patches as mpatches


dir_loc = 'C:/Users/Lifeng Liu/Desktop/bar_chart_race_python_project/'
current_date = datetime.date.today() # "2020-04-04"


# Read Dataset
df_original = pd.read_csv(dir_loc + '/total-cases-covid-19.csv', 
                 usecols=['Entity', 'Code', 'Date', 'Total confirmed cases of COVID-19 (cases)']) 
# date source: https://ourworldindata.org/coronavirus-data
# alternative data source: https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
# reformat the date from string to date

df_csv = pd.DataFrame(data=df_original)
df_csv.rename(columns = {'Date':'old_format_date'}, inplace = True) 
df_csv['old_format_date']=df_csv['old_format_date'].str.replace(",","")
df_csv.insert(4,"Date",[current_date]*len(df_csv['old_format_date']))


for i in range(len(df_csv['old_format_date'])):
   df_csv["Date"][i]=datetime.datetime.strptime(df_csv['old_format_date'][i], '%b %d %Y').strftime('%Y-%m-%d')
    

# reformat the csv from long format to wide format with pandas pivot function. Use pandas melt function for wide to long format conversion.
transposed_csv = df_csv.pivot(index="Entity", columns="Date", values="Total confirmed cases of COVID-19 (cases)")


df_country = pd.read_csv(dir_loc + '/countries_and_regions_flag_info_updated_local_image.csv',
                         usecols=['Entity', 'region','ImagePath','Color']) 

# merge the confirmed cases with country info.
df=pd.merge(transposed_csv, df_country, on="Entity") # this merge removes country or regions without continent info or flag info.
df=df.fillna(0) # replace NaN values in cases with zeros



# plot setting

fig, ax = plt.subplots(figsize=(28, 12))

colors = dict(zip(
    ['Asia', 'Europe', 'Africa', 'Americas', 'Oceania'],
    ['#adb0ff','#f7bb5f' , '#90d595', '#e48381', '#aafbff']))
group_lk = df.set_index('Entity')['region'].to_dict()

font = {'family' : 'sans serif','weight' : 10, 'size'   : 15} # check https://matplotlib.org/3.2.1/tutorials/text/text_props.html for more details

def drawChart(date):
    # get the world total cases
    df2 = df_csv[(df_csv["Entity"]=="World") & (df_csv["Date"]==date)].set_index("Entity", drop = False) 
    world_total=df2.loc["World","Total confirmed cases of COVID-19 (cases)"]    
    # extract the info of top 10 countries and regions
    df.sort_values(by = str(date), ascending = False, inplace=True)
    ax.clear() 
    country = df.iloc[:,0].head(10)
    case = df[str(date)].head(10)
    color_set = [colors[group_lk[x]] for x in country]
    imagesPath = df['ImagePath'].head(10)
    ax.barh(country, case, align='center', color=color_set)    
    dx = case.max() / 40
    for i,(c,iP) in enumerate(zip(case,imagesPath)):
        ax.text(c+0.5*dx, i, f"{c:,.0f}",  size=20, color='#777777', ha='left',  va='center')
        # Figure
        flag = img.imread(str(iP))
        imagebox = OffsetImage(flag, zoom=0.09)
        ab = AnnotationBbox(imagebox, (c- 0.6*dx, i),frameon=False, bboxprops =dict(edgecolor=None,color=None,boxstyle="square,pad=0.1")) # edgecolor and color set as None to make a transparent background.
        ax.add_artist(ab)

    # Axis Configuration ... polished styles
    ax.invert_yaxis()
    plt.box(False)
    plt.rc('font', **font)
    ax.text(1, 0.3, date, transform=ax.transAxes, color='#777777', size=60, ha='right', weight=800)
    ax.text(1, 0.1, f"World Total: {world_total}", transform=ax.transAxes, color='#777777', size=40, ha='right', weight=500)        
    ax.text(-0.08, 1.01, 'Confirmed cases', transform=ax.transAxes, size=13, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=15) # Change the appearance of ticks, tick labels, and gridlines.
    ax.tick_params(axis='y', colors='#777777', labelsize=12) 
    ax.set_yticklabels(country, fontdict = font)
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(1, 0, f'by @Lifeng Liu; {current_date}', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    
    # Add the legend manually to the current Axes. http://matplotlib.org/users/legend_guide.html 
    Asia_patch = mpatches.Patch(color='#adb0ff', label='Asia')
    Europe_patch = mpatches.Patch(color='#f7bb5f', label='Europe')
    Africa_patch = mpatches.Patch(color='#90d595', label='Africa')
    Americas_patch = mpatches.Patch(color='#e48381', label='Americas')
    Oceania_patch = mpatches.Patch(color='#aafbff', label='Oceania')
    
    Asia_legend=plt.legend(handles=[Asia_patch], frameon=False, bbox_to_anchor=(0, 1.1), fontsize=13)
    Europe_legend=plt.legend(handles=[Europe_patch], frameon=False,bbox_to_anchor=(0.055, 1.1), fontsize=13)
    Africa_legend=plt.legend(handles=[Africa_patch], frameon=False,bbox_to_anchor=(0.105, 1.1), fontsize=13)
    Americas_legend=plt.legend(handles=[Americas_patch], frameon=False,bbox_to_anchor=(0.17, 1.1), fontsize=13)
    Oceania_legend=plt.legend(handles=[Oceania_patch], frameon=False,bbox_to_anchor=(0.23, 1.1), fontsize=13)

    plt.gca().add_artist(Asia_legend)  
    plt.gca().add_artist(Europe_legend)  
    plt.gca().add_artist(Africa_legend)  
    plt.gca().add_artist(Americas_legend)  
    plt.gca().add_artist(Oceania_legend)  
    
    plt.box(False)    
# end drawChart function
    


# sinle plot check 
# drawChart("2020-03-24")


"""
# draw separate images


for date in datelist:
    drawChart(date)
    plt.savefig(dir_loc+ date +".png")


"""


#Animate Race
fig, ax = plt.subplots(figsize=(28, 12))
# Extract dates
dates = df.columns[1:-3]
animator = animation.FuncAnimation(fig, drawChart,frames=dates, interval=500, repeat = False) 
animator.save(dir_loc+f"{current_date} top 10 countries & regions with COVID-19 cases confirmed.gif")
