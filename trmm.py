#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:11:23 2017

@author: taylor
"""

#def daterange(start_date, end_date):
#    for n in range(int ((end_date - start_date).days)):
#        yield start_date + timedelta(n)

def trmmload():
    mainDir = "/home/taylor/trmm/"
    import numpy as np
    import os
    from datetime import date, timedelta
    import fnmatch
    startDate = date(2000,3,1)
    ensoP = np.empty((1,79,66))
    ensoNeu= np.empty((1,79,66))
    newDate=startDate
    c1=0
    c2=0
    c3=0
    for file in os.listdir(mainDir):
        if fnmatch.fnmatch(file,'*.nc4*'):
            if c1 == 0 and c2 == 0 and c3 == 0:
                lats,lons = netcdfLatLonLoad(file)
            precip = netcdfLoad(file)
                
            count = -50
            
            oniVal = ensoSubset(mainDir,newDate)
           
            if oniVal > 0.5:
                
                if precip is not None:
                    try:
                        if count == oniVal:
                            continue
                        if c1 ==0:
                            ensoPos= np.expand_dims(precipMash(precip),axis=0)
                            ensoP = ensoPos
                        else:
                            ensoPos = np.expand_dims(precipMash(precip),axis=0)
                            if ensoPos is None:
                                ensoP = np.append(ensoP,np.mean(ensoP),axis=0)
                            else:
                                ensoP = np.append(ensoP,ensoPos,axis=0)
                    except ValueError:
                        print('uhoh')
                    count=oniVal
                    c1+=1
                if precip is None:
                     ensoP = np.append(ensoP,np.mean(ensoP),axis=0)
            elif oniVal < -0.5:
                
                if precip is not None:
                    try:
                        if count == oniVal:
                            continue
                        if c2 ==0:
                            ensoMin = np.expand_dims(precipMash(precip),axis=0)
                            ensoM = ensoMin
                        else:
                            ensoMin = np.expand_dims(precipMash(precip),axis=0)
                            if ensoMin is None:
                                ensoM = np.append(ensoM,np.mean(ensoM),axis=0)
                            else:
                                ensoM = np.append(ensoM,ensoMin,axis=0)
                    except ValueError:
                        print('uhoh')
                    count=oniVal
                    c2+=1
                if precip is None:
                     ensoM = np.append(ensoM,np.mean(ensoM),axis=0)
            elif -0.5<=oniVal<=0.5:
                if precip is not None:
                    try:
                        if count == oniVal:
                            continue
                        if c3==0:
                            ensoNeutral = np.expand_dims(precipMash(precip),axis=0)
                            ensoNeu = ensoNeutral
                        else:
                            ensoNeutral = np.expand_dims(precipMash(precip),axis=0)
                            if ensoNeutral is None:
                                ensoNeu = np.append(ensoNeu,np.mean(ensoNeu),axis=0)
                            else:
                                ensoNeu = np.append(ensoNeu,ensoNeutral,axis=0)
                    except ValueError:
                        print('uhoh')
                    count=oniVal
                    c3+=1
                if precip is None:
                    ensoNeu = np.append(ensoNeu,np.mean(ensoNeu),axis=0)
                    
            newDate=newDate + timedelta(days=1)
            
    print(ensoNeu.shape)
    print(ensoM.shape)
    print(ensoP.shape)
    mapMaker(ensoNeu,ensoM,ensoP,lats,lons)
                        
            
def mapMaker(ensoNeu,ensoM,ensoP,lats,lons):
    import matplotlib.pyplot as plt
    import numpy as np
    import cartopy.crs as ccrs
    import cartopy.feature as ft
    import seaborn as sns
    
    
    
    bigArr = np.append(ensoNeu,ensoM,axis=0)   
    bigArr = np.append(bigArr,ensoP,axis=0)
    bigArrMean = np.mean(bigArr,axis=0)
    ensoNeu = np.mean(ensoNeu,axis=0)
    ensoM = np.mean(ensoM,axis=0)
    ensoP=np.mean(ensoP,axis=0)
    
    sns.distplot(ensoNeu.flatten(),bins=20,color='blue')
    sns.distplot(ensoM.flatten(),bins=20,color='red')
    sns.distplot(ensoP.flatten(),bins=20,color='green')
    plt.figure(figsize=(10,5))
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution=('110m'))
    x,y=np.meshgrid(lons,lats)
    ax.add_feature(ft.BORDERS,linestyle=':',alpha=0.5)    
    cf=ax.contourf(x,y,bigArrMean,np.linspace(0,30,num=11),transform=ccrs.PlateCarree(),cmap=plt.cm.viridis)
    cbar=plt.colorbar(cf,ticks=np.linspace(0,30,num=11))
    cbar.set_label('mm/day')
    ax.plot(-75.590556,6.230833, 'wo', markersize=3)
    ax.text(-75.3, 6.4, 'Medellin',color='w')
    plt.show()
    plt.close('all')
    
    plt.figure(figsize=(10,5))
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution=('110m'))
    x,y=np.meshgrid(lons,lats)
    ax.add_feature(ft.BORDERS,linestyle=':',alpha=0.5)    
    cf=ax.contourf(x,y,ensoNeu,np.linspace(0,30,num=11),transform=ccrs.PlateCarree(),cmap=plt.cm.viridis)
    cbar=plt.colorbar(cf,ticks=np.linspace(0,30,num=11))
    cbar.set_label('mm/day')
    ax.plot(-75.590556,6.230833, 'wo', markersize=3)
    ax.text(-75.3, 6.4, 'Medellin',color='w')
    plt.show()
    plt.close('all')
    
    plt.figure(figsize=(10,5))
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution=('110m'))
    x,y=np.meshgrid(lons,lats)
    ax.add_feature(ft.BORDERS,linestyle=':',alpha=0.5)    
    cf=ax.contourf(x,y,ensoP,np.linspace(0,30,num=11),transform=ccrs.PlateCarree(),cmap=plt.cm.viridis)
    cbar=plt.colorbar(cf,ticks=np.linspace(0,30,num=11))
    cbar.set_label('mm/day')
    ax.plot(-75.590556,6.230833, 'wo', markersize=3)
    ax.text(-75.3, 6.4, 'Medellin',color='w')
    plt.show()
    plt.close('all')
    
    plt.figure(figsize=(10,5))
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution=('110m'))
    x,y=np.meshgrid(lons,lats)
    ax.add_feature(ft.BORDERS,linestyle=':',alpha=0.5)    
    cf=ax.contourf(x,y,ensoM,np.linspace(0,30,num=11),transform=ccrs.PlateCarree(),cmap=plt.cm.viridis)
    cbar=plt.colorbar(cf,ticks=np.linspace(0,30,num=11))
    cbar.set_label('mm/day')
    ax.plot(-75.590556,6.230833, 'wo', markersize=3)
    ax.text(-75.3, 6.4, 'Medellin',color='w')
    plt.show()
    plt.close('all')
    
    plt.figure(figsize=(10,5))
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution=('110m'))
    x,y=np.meshgrid(lons,lats)
    ax.add_feature(ft.BORDERS,linestyle=':',alpha=0.5)    
    cf=ax.contourf(x,y,ensoM,np.linspace(0,30,num=11),transform=ccrs.PlateCarree(),cmap=plt.cm.viridis)
    cbar=plt.colorbar(cf,ticks=np.linspace(0,30,num=11))
    cbar.set_label('mm/day')
    ax.plot(-75.590556,6.230833, 'wo', markersize=3)
    ax.text(-75.3, 6.4, 'Medellin',color='w')
    plt.show()
    plt.close('all')
    #for val in cf.collections:
    #    val.remove()
    
def netcdfLoad(file):
    from netCDF4 import Dataset
    try:
        a = Dataset(file)
    except OSError:
        import pdb
        pdb.set_trace()
    precip = a.variables['precipitation']
    return precip

def netcdfLatLonLoad(file):
    from netCDF4 import Dataset
    try:
        a = Dataset(file)
    except OSError:
        import pdb
        pdb.set_trace()

    lats = a.variables['lat'][:]
    lons = a.variables['lon'][:]
    return lats,lons

def precipMash(prcp):
    import numpy as np
    try:
        masterPrcpArray = np.array(prcp).T    
    except RuntimeError:
        masterPrcpArray= None
    return masterPrcpArray

def ensoSubset(mainDir,dateVal):
    import numpy as np
    from datetime import date
    startDate = date(2000,3,1)
    curMonth = (dateVal.month+((dateVal.year-startDate.year)*12)) - startDate.month
    oni = np.loadtxt(mainDir+'oni.txt')
    oni=np.delete(oni,(0),axis=1)
    oni=oni.flatten()

    for x in range(len(oni)):
        if curMonth == x:
            if oni[x] is None:
                import pdb
                pdb.set_trace()
            return oni[x]
        elif curMonth != x:
            if oni[x] is None:
                import pdb
                pdb.set_trace()
            continue
        if oni[x] is None:
                import pdb
                pdb.set_trace()

    
            
if __name__ == '__main__':
    trmmload()
    
    
    
    
                    
    
    
           