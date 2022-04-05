#!/usr/bin/env python3

import pandas as pd
from matplotlib import pyplot as plt
from cartopy import crs as ccrs
from datetime import datetime as dt, timedelta
from metpy.plots import USCOUNTIES

lmaData = pd.read_csv("selected_lma_matlab_20220109_1.csv")
startDate = dt(2022, 1, 9, 0, 0, 0, 0)
pyDateTimes = list()
for numSeconds in lmaData["Second Fraction"]:
    timeOfPoint = startDate + timedelta(seconds=numSeconds)
    pyDateTimes.append(timeOfPoint)
lmaData["pyDateTimes"] = pyDateTimes
lmaData = lmaData.set_index(["pyDateTimes"])
listOfTimes = list()
currentTime = startDate
while currentTime < startDate + timedelta(days=1):
    fiveMinBin = lmaData[(lmaData.index >= currentTime) & (lmaData.index <= (currentTime + timedelta(minutes=5)))]
    listOfTimes.append(currentTime)
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    sctPlot = ax.scatter(fiveMinBin["K"], fiveMinBin["J"], s=0.2, c=fiveMinBin["Second Fraction"], cmap="rainbow")
    fig.colorbar(sctPlot, label="Second Fraction")
    ax.add_feature(USCOUNTIES.with_scale("5m"), edgecolor="gray")
    ax.set_extent([-99.5, -91, 26, 33.5])
    px = 1/plt.rcParams["figure.dpi"]
    fig.set_size_inches(1920*px, 1080*px)
    fig.savefig(str(currentTime)+".png")
    currentTime = currentTime + timedelta(minutes=5)
