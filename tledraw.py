#!/usr/bin/env python
# -*- coding: utf-8 -*-

import predict
import time
import datetime
from time import gmtime, strftime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

passImgDir='/opt/wxsat/passes'

NOAA15=[]
NOAA18=[]
NOAA19=[]
ktore=[ NOAA15, NOAA18, NOAA19 ]
g = []

tlefile=open('/tmp/weather.txt', 'r')
tledata=tlefile.readlines()
tlefile.close()

for i, line in enumerate(tledata):
    if "NOAA 15" in line: 
        for l in tledata[i:i+3]: NOAA15.append(l.strip('\r\n').rstrip()),
for i, line in enumerate(tledata):
    if "NOAA 18" in line: 
        for m in tledata[i:i+3]: NOAA18.append(m.strip('\r\n').rstrip()),
for i, line in enumerate(tledata):
    if "NOAA 19" in line: 
        for n in tledata[i:i+3]: NOAA19.append(n.strip('\r\n').rstrip()),

qth = (53.34045, -15.05793, 5)

font = {'color':  'blue',
        'size': 8,
        }

czasStart=time.time()
czasKoniec=time.time()+86400
minEl=14
printEl=0

for h in ktore:
    print h[0]
    p = predict.transits(h, qth, czasStart)
    for i in range(1,20):
	transit = p.next()
	minuty=time.strftime("%M:%S", time.gmtime(transit.duration()))
	if int(transit.peak()['elevation'])>=minEl:
	    f=predict.quick_predict(h,transit.start,qth)
	    XP=[]
	    YP=[]
	    CZAS=[]
	    TABELA=[]
	    nazwa=f[0]['name']
	    for md in f:
		YP.append(90-md['elevation'])
		XP.append(md['azimuth'])
	        CZAS.append(int(md['epoch']))
	    for ed,ag in enumerate(XP):
		TABELA.append({'czas': strftime('%H:%M:%S', time.localtime(CZAS[ed])), 'azi': np.radians(XP[ed]),'elev': YP[ed]})
	    theta=np.radians(XP)
	    zeniths=YP
	    plt.ioff()
	    ax = matplotlib.pyplot.figure(figsize=(4.0, 4.0))
	    ax = plt.subplot(111, projection='polar')  # create figure & 1 axis
	    ax.set_xticklabels(['', '', '', '', '', '', '', ''])
	    ax.set_yticklabels(['90','','','','','','','0'])
	    gridX,gridY = 10.0,15.0
	    parallelGrid = np.arange(-90.0,90.0,gridX)
	    meridianGrid = np.arange(-180.0,180.0,gridY)
	    ax.text(0.5,1.025,'N',transform=ax.transAxes,horizontalalignment='center',verticalalignment='bottom',size=12)
	    for para in np.arange(gridY,360,gridY):
	        x= (1.1*0.5*np.sin(np.deg2rad(para)))+0.5
	        y= (1.1*0.5*np.cos(np.deg2rad(para)))+0.5
	        ax.text(x,y,u'%i\N{DEGREE SIGN}'%para,transform=ax.transAxes,horizontalalignment='center',verticalalignment='center',size=10)
	    ax.set_aspect(1.0)
	    ax.set_rmax(90)
	    ax.set_theta_zero_location("N")
	    ax.set_theta_direction(-1)
	    ax.plot(theta,zeniths)
	    dc=0.01
	    for mc in TABELA:
		ax.text(mc['azi'],mc['elev'],mc['czas']+' '+str(int(mc['elev']))+'$^\circ$',fontdict=font)
	    plt.savefig(passImgDir+'/'+nazwa+'-'+str(strftime('%Y%m%d-%H%M',time.localtime(transit.start)))+'-pass-map.png')   # save the figure to file
	    plt.close()    # close the figure
	    print "** "+strftime('%d-%m-%Y %H:%M:%S', time.localtime(transit.start))+" ("+str(int(transit.start))+") to "+strftime('%d-%m-%Y %H:%M:%S', time.localtime(transit.start+int(transit.duration())))+" ("+str(int(transit.start+int(transit.duration())))+")"+", dur: "+str(int(transit.duration()))+" sec ("+str(minuty)+"), max el. "+str(int(transit.peak()['elevation']))+" deg."
	else:
	    if str(printEl) in "1":
		print "!! "+strftime('%d-%m-%Y %H:%M:%S', time.localtime(transit.start))+" ("+str(int(transit.start))+") to "+strftime('%d-%m-%Y %H:%M:%S', time.localtime(transit.start+int(transit.duration())))+" ("+str(int(transit.start+int(transit.duration())))+")"+", dur:"+str(int(transit.duration()))+"s. ,max "+str(int(transit.peak()['elevation']))+" el."
