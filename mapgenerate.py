import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import ee

data=gpd.read_file('map.shp')
dats=pd.read_csv('dataset.csv')
dats['nontap']=0
dats['tot']=0
for i in dats.columns:
    if i not in ['Mun','Ward','Tap/piped water (within premises)','Tap/piped water (outside premises)','nontap','tot']:
        dats['nontap']+=dats[i]
        print(i)
    if i not in ['Mun','Ward','nontap','tot']:
        dats['tot']+=dats[i]
dats['perct']=dats['nontap']/dats['tot']*100
print(dats)
print(dats['perct'].max(),dats['perct'].min(),dats['perct'].mean(),dats['perct'].std())
print(dats)




def colorsender(dats):
    dats['col']=''
    x=dats['perct'].mean()
    y=dats['perct'].std()
    print(x,y)
    col=['#ffffff','#ff8080','#ff3333','#b30000','#4d0000']
    ranges=[x-y,x-0.5*y,x,x+0.5*y,x+y]
    print(ranges)
    for i in range(len(dats)):
        if dats.iloc[i]['perct']<ranges[0]:
            dats.at[dats.index[i],'col']=col[0]
        if dats.iloc[i]['perct']>ranges[0]:
            if dats.iloc[i]['perct']<ranges[1]:
                dats.at[dats.index[i],'col']=col[1]
            elif dats.iloc[i]['perct']<ranges[2]:
                dats.at[dats.index[i],'col']=col[2]
            elif dats.iloc[i]['perct']<ranges[3]:
                dats.at[dats.index[i],'col']=col[3]
            else:
                dats.at[dats.index[i],'col']=col[4]
    return dats
print(data)
dats=colorsender(dats)

for i in range(len(data)):
    shapes=data.loc[data.index[i],'geometry']
    try:
        print(dats.loc[(data.loc[data.index[i],'PALIKA']==dats['Mun'])&(data.loc[data.index[i],'WARD']==dats['Ward'])].iloc[0]['col'])
        filla=dats.loc[(data.loc[data.index[i],'PALIKA']==dats['Mun'])&(data.loc[data.index[i],'WARD']==dats['Ward'])].iloc[0]['col']
    except:
        filla='black'
    if shapes.geom_type=='MultiPolygon':
            li=list(shapes.geoms)
            for j in li:        
                x,y = j.exterior.xy
                plt.plot(x,y, linewidth=0.3)
                plt.fill(x,y,filla,alpha=.5)
                a,b=j.centroid.xy
                plt.text(a[0],b[0],str(data.loc[data.index[i],'WARD']))
    else:
        x,y = shapes.exterior.xy
        plt.plot(x,y, linewidth=0.3)
        plt.fill(x,y,filla,alpha=.5)
        a,b=shapes.centroid.xy
        print(a,b)
        plt.text(a[0],b[0],str(data.loc[data.index[i],'WARD']) )

x=dats['perct'].mean()
y=dats['perct'].std()
print(x,y)
col=['#ffffff','#ff8080','#ff3333','#b30000','#4d0000']
ranges=[round(x-y),round(x-0.5*y),round(x),round(x+0.5*y),round(x+y)]
ranges=[round(x-y),round(x-0.5*y),round(x),round(x+0.5*y),round(x+y)]
labes=[str(ranges[0]),str(ranges[0])+'-'+str(ranges[1]),str(ranges[1])+'-'+str(ranges[2]),str(ranges[3])+'-'+str(ranges[4]),'Greater than '+str(ranges[4])]
for i in range(len(labes)):
    filla=col[i]
    plt.fill(a[0],b[0],filla,alpha=.5,label=labes[i]+'%')
plt.title('Percentage of Households Dependant on Water sources other than Tap water in Chaurjahari Municipality')
plt.legend()
print(dats)
#data.plot()
#plt.savefig('data.pdf')
plt.show()
