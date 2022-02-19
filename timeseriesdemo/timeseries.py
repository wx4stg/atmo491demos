import pandas as pd
from datetime import datetime as dt, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates as pltdates

hlmaData = pd.read_csv("hlma_211218_flash_1.csv")
startOfDay = dt(2021, 12, 18, 0, 0, 0, 0)
flashDtsList = list()
for numSeconds in hlmaData["Second Fraction"]:
    timeOfFlash = startOfDay + timedelta(seconds=numSeconds)
    flashDtsList.append(timeOfFlash)
hlmaData["pyDateTimes"] = flashDtsList
hlmaData = hlmaData.set_index(["pyDateTimes"])
currentTime = startOfDay
listOfTimes = list()
listOfCounts = list()
while currentTime < startOfDay + timedelta(days=1):
    fiveMinBin = hlmaData[(hlmaData.index >= currentTime) & (hlmaData.index <= (currentTime + timedelta(minutes=5)))]
    listOfTimes.append(currentTime)
    listOfCounts.append(len(fiveMinBin))
    currentTime = currentTime + timedelta(minutes=5)
fig = plt.figure()
ax = fig.gca()
ax.plot(listOfTimes, listOfCounts, "black")
ax.xaxis.set_major_formatter(pltdates.DateFormatter("%H:%M"))
fig.suptitle("HLMA Flash Count -- 18 December 2021")
ax.set_xlabel("Time (UTC)")
ax.set_ylabel("HLMA VHF Flashes (per 5 minutes)")
fig.savefig("output.png")
