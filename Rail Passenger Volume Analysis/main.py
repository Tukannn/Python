#Copyright (C) 2022 Jakub Jura
#Accenture recruitment task


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Define path and read source file
path = r''
filename = r'Rail.csv'
df = pd.read_csv(path+filename, header=0, thousands=',')
df = df.rename(columns={"GEO/TIME": "Year"})
df = df.set_index('Year')
df = df.T
df = df.rename(columns={"Germany (until 1990 former territory of the FRG)": "Germany"})

#Convert empty fields to 0
df = df.replace(':','0')

#Convert strings to numeric
df = df.replace({',': ''}, regex = True).astype(int) #Source https://sparkbyexamples.com/pandas/pandas-convert-string-to-float-type-dataframe/

#Drop not-meaningful columns
df = df.drop(columns = ['European Union - 27 countries (from 2020)', 'European Union - 28 countries (2013-2020)', 'European Union - 27 countries (2007-2013)'])

#Choose columns to plot
x=["Powietrze","Olej","Woda"]
y = (3.75,	15.00,	21.40)
xpos = np.arange(len(y))
y1 = (13.40, 13.40, 13.40)
y2 = df['Czechia'].dropna()
y3 = df['Denmark'].dropna()
y4 = df['Germany'].dropna()
y5 = df['Estonia'].dropna()
y6 = df['Ireland'].dropna()
y7 = df['Greece'].dropna()
y8 = df['Spain'].dropna()
y9 = df['France'].dropna()
y10 = df['Croatia'].dropna()
y11 = df['Italy'].dropna()
y12 = df['Latvia'].dropna()
y13 = df['Lithuania'].dropna()
y14 = df['Luxembourg'].dropna()
y15 = df['Hungary'].dropna()
y16 = df['Austria'].dropna()
y17 = df['Poland'].dropna()
y18 = df['Portugal'].dropna()
y19 = df['Romania'].dropna()
y20 = df['Slovenia'].dropna()
y21 = df['Slovakia'].dropna()
y22 = df['Finland'].dropna()
y23 = df['Sweden'].dropna()
y24 = df['Liechtenstein'].dropna()
y25 = df['Norway'].dropna()
y26 = df['Switzerland'].dropna()
y27 = df['United Kingdom'].dropna()
y28 = df['Montenegro'].dropna()
y29 = df['North Macedonia'].dropna()
y30 = df['Türkiye'].dropna()
y31 = df['Bosnia and Herzegovina'].dropna()
y32 = df['Total']



#Define additional data
countries = list(df.columns)

#Choose error colums
#x_error =
#y_error = df[''].dropna()
OC_error=[	1.126,	5.840,	3.344]
POC_error=[1.087, 1.087, 1.087]

#Colors
#colors = sns.color_palette("rocket", 1)
colors = sns.cubehelix_palette(31, start=.5, rot=-.75)
colors_s = sns.cubehelix_palette(10, start=.5, rot=-.75)

#Create figure
fig = plt.figure(1, figsize=(6, 4))
#plt.plot(x, y32, linestyle='', marker='^', label='', color=colors[30], mfc='w', markersize=10)
plt.bar(x, y, yerr=OC_error, color=colors[10], ec="black", capsize=4, width=0.25, label='Po OC')
plt.bar(xpos-.25, y1, yerr=POC_error, color=colors[1], ec="black", capsize=4, width=0.25, label='Przed OC')
#plt.stackplot(x,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15,y16,y17,y18,y19,y20,y21,y22,y23,y24,y25,y26,y27,y28,y29,y30,y31, labels=countries, colors = colors)


#Plot parameters
#plt.xlim(0,9)
plt.ylim(0,30)
plt.minorticks_off()
plt.tick_params(direction='in', right=True, top=True)
plt.tick_params(labelsize=14)
plt.tick_params(labelbottom=True, labeltop=False, labelright=False)
xticks = np.arange(0,3,1)
yticks = np.arange(0,31,5)

plt.tick_params(direction='in', which='minor', length=3, bottom=False, top=False, right=False, left=True)
plt.tick_params(direction='in', which='major', length=6, bottom=True, top=True, right=True)
plt.xticks(xticks)
plt.yticks(yticks)

#Add label
plt.xlabel('', fontsize=14)
plt.ylabel('HRC', fontsize=14)

#Add text and line on top of figure
#plt.axvline(x=7, linestyle = 'dotted', color = 'black')
#plt.text(6.7, 150000, r'COVID-19 Pandemic', rotation = 90, fontsize=14)



#Add legend
plt.legend(bbox_to_anchor = (0.4, 0.98), fontsize=14)

#Save figue
plt.savefig('Plots_Output/HRC.png', dpi=300, bbox_inches="tight")




#Show plot
plt.show()
