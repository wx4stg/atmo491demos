#!/usr/bin/env python3
# Azimuth-Elevation plotting for selected HLMA data
# Created 6 March 2022 by Sam Gardner <stgardner4@tamu.edu>
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import image as mpimage
from datetime import datetime as dt, timedelta
from os import path
from pathlib import Path

if __name__ == "__main__":
    baseDir = path.dirname(path.abspath(__file__))
    allData = pd.read_csv("selected_lma_print_20210914.txt", comment="#")
    allData["t(mus)"] = pd.to_numeric(allData["t(mus)"], errors="coerce")
    allData = allData.dropna(how="any")
    startTime = dt(2021, 9, 14, 0, 0, 0, 0)
    allData["pydatetimes"] = [startTime + timedelta(microseconds=microsec) for microsec in allData["t(mus)"]]
    allData = allData.set_index(["pydatetimes"])
    outDir = path.join(baseDir, "output")
    Path(outDir).mkdir(parents=True, exist_ok=True)
    finalTime = allData.index[-1]

    while startTime < finalTime:
        endTime = startTime + timedelta(minutes=10)
        selectedData = allData[startTime:endTime]
        selectedData["secInBin"] = [((currentTime-startTime).total_seconds()/(endTime-startTime).total_seconds())*(endTime-startTime).total_seconds() for currentTime in selectedData.index]
        print(selectedData)
        fig = plt.figure()
        px = 1/plt.rcParams["figure.dpi"]
        fig.set_size_inches(1920*px, 1080*px)
        ax = plt.axes(polar=True)
        ax.set_theta_direction(-1)
        ax.set_theta_offset(np.pi/2)
        scatterHandle = ax.scatter(selectedData["Azim"], selectedData["Elev"], c=selectedData["secInBin"], s=0.1, cmap="rainbow", vmin=0, vmax=600)
        ax.set_ylim(0, 90)
        ax.set_position([ax.get_position().x0, 0.95-ax.get_position().height, ax.get_position().width, ax.get_position().height])
        cbax = fig.add_axes([.05, 0.075, (ax.get_position().width/3), .02])
        cb = fig.colorbar(scatterHandle, orientation="horizontal", cax=cbax, label="Seconds after "+startTime.strftime("%-d %b %Y %H%MZ"))
        cb.set_ticks(range(0, 601, 60))
        cbax.set_position([.05, .1-cbax.get_position().height, cbax.get_position().width, cbax.get_position().height])
        tax = fig.add_axes([0,0,(ax.get_position().width/3),.05])
        tax.text(0.5, 0.5, "Houston LMA 10-minute VHF Flashes\nValid "+startTime.strftime("%-d %b %Y %H%MZ")+" through "+endTime.strftime("%H%MZ"), horizontalalignment="center", verticalalignment="center", fontsize=16)
        tax.axis("off")
        tax.set_position([(ax.get_position().width/2)-(tax.get_position().width/2)+ax.get_position().x0,ax.get_position().y0-.07-tax.get_position().height,tax.get_position().width,tax.get_position().height], which="both")
        lax = fig.add_axes([0,0,(ax.get_position().width/3),1])
        lax.set_aspect(2821/11071)
        lax.axis("off")
        plt.setp(lax.spines.values(), visible=False)
        atmoLogo = mpimage.imread("assets/atmoLogo.png")
        lax.imshow(atmoLogo)
        lax.set_position([.95-lax.get_position().width, .1-lax.get_position().height, lax.get_position().width, lax.get_position().height], which="both")
        figSavePath = path.join(outDir, startTime.strftime("%H%M")+".png")
        fig.savefig(figSavePath)
        startTime = startTime + timedelta(minutes=10)
