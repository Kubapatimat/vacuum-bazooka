from bazooka_measurements import measurements
from bazooka import Bazooka
from constants import m, r, C, x0, y0, l, g
import numpy as np
from math import degrees, radians
from plot_utils import drawPlots, drawComparisonPlots
import jsonpickle
import os.path


def main():
    calculatedBazookaList = getCalculatedBazookaList("data.txt")
    averageBazookaList = getAverageBazookaList(calculatedBazookaList)
    printBazookaListInfo(averageBazookaList)

    averageDistanceBazookaList = getBazookaOfSomeKindList(
        'distanceBazooka', averageBazookaList)
    averageTimeBazookaList = getBazookaOfSomeKindList(
        'timeBazooka', averageBazookaList)
    distanceBazookaComparisonList = getBazookaOfSomeKindComparisonList(
        'distanceBazooka', averageBazookaList)
    timeBazookaComparisonList = getBazookaOfSomeKindComparisonList(
        'timeBazooka', averageBazookaList)

    drawComparisonPlots(distanceBazookaComparisonList,
                        "Comparison of the bullet's position calculated using range measurements in both cases",
                        angleInformation, "Ignoring air resistance", "Taking air resistance into account")

    drawComparisonPlots(timeBazookaComparisonList,
                        "Comparison of the bullet's position calculated using time measurements in both cases",
                        angleInformation, "Ignoring air resistance", "Taking air resistance into account")

    drawPlots(averageDistanceBazookaList,
              "Position calculated using range measurements (taking air resistance into account)", angleInformation)

    drawPlots(averageTimeBazookaList,
              "Position calculated using time measurements (taking air resistance into account)", angleInformation)


def getBazookaOfSomeKindList(bazookaName, bazookaList):
    averageBazookaOfSomeKindList = [averageBazooka[bazookaName]
                                    for averageBazooka in bazookaList]

    return averageBazookaOfSomeKindList


def getBazookaOfSomeKindComparisonList(bazookaName, bazookaList):
    averageBazookaOfSomeKindList = getBazookaOfSomeKindList(
        bazookaName, bazookaList)

    bazookaOfSomeKindWithoutAirResistanceList = [Bazooka(m=m, r=r, C=0, alpha=degrees(
        averageBazookaOfSomeKind.alpha), x0=x0, y0=y0, v0=averageBazookaOfSomeKind.v0).solve() for
        averageBazookaOfSomeKind in averageBazookaOfSomeKindList]

    bazookaOfSomeKindComparisonList = list(map(lambda i: [bazookaOfSomeKindWithoutAirResistanceList[i]] + [
        averageBazookaOfSomeKindList[i]], range(len(bazookaOfSomeKindWithoutAirResistanceList))))

    return bazookaOfSomeKindComparisonList


def getCalculatedBazookaList(fileName, writeToFile=True):
    if os.path.isfile(fileName):
        with open(fileName, 'r') as outfile:
            return jsonpickle.decode(outfile.read())
    else:
        calculatedBazookaList = []
        for measurementIndex, measurement in enumerate(measurements):
            angle = measurement.getAngle(y0, l)
            s = measurement.s

            distanceBazookaObjects = []
            timeBazookaObjects = []

            for i, (offset, time, v0Guess) in enumerate(
                zip(measurement.distanceList,
                    measurement.timeList, measurement.v0GuessList)
            ):
                timeCorrection = measurements[measurementIndex].timeCorrectionList[
                    i]if measurements[measurementIndex].timeCorrectionList != None else 0

                distanceBazooka = Bazooka(m=m, r=r, C=C, alpha=angle, x0=x0, y0=y0, z=(
                    s+offset)).solve(v0Guess)

                timeBazooka = Bazooka(m=m, r=r, C=C, alpha=angle, x0=x0, y0=y0, T=(
                    time + timeCorrection)).solve(v0Guess)

                distanceBazookaObjects.append(distanceBazooka)
                timeBazookaObjects.append(timeBazooka)

            calculatedBazookaList.append(
                {"distanceBazookaList": distanceBazookaObjects, "timeBazookaList": timeBazookaObjects})

        if (writeToFile):
            with open(fileName, 'w') as outfile:
                outfile.write(jsonpickle.encode(calculatedBazookaList))

        return calculatedBazookaList


def getAverageBazookaList(calculatedBazookaList):
    averageBazookaList = []
    for index, calculatedBazooka in enumerate(calculatedBazookaList):
        averageBazookaTypeDict = {}
        for calculatedBazookaType in ["distanceBazookaList", "timeBazookaList"]:
            calculatedBazookaTypeList = calculatedBazooka.get(
                calculatedBazookaType)
            averageVelocity = np.average(
                [bazookaType.v0 for bazookaType in calculatedBazookaTypeList])

            averageBazooka = Bazooka(m=calculatedBazookaTypeList[0].m, r=calculatedBazookaTypeList[0].r,
                                     C=calculatedBazookaTypeList[0].C, alpha=degrees(
                                         calculatedBazookaTypeList[0].alpha),
                                     x0=calculatedBazookaTypeList[0].x0, y0=calculatedBazookaTypeList[0].y0,
                                     v0=averageVelocity).solve()

            keyName = calculatedBazookaType[0:-4]

            averageBazookaTypeDict[keyName] = averageBazooka
        averageBazookaList.append(averageBazookaTypeDict)

    return averageBazookaList


def printBazookaListInfo(bazookaList):
    def printTitle(title):
        print("-"*(len(title)+2))
        print(" " + title)
        print("-"*(len(title)+2))
        print()

    printTitle("Range measurements")

    for i, bazooka in enumerate(bazookaList):
        bazooka['distanceBazooka'].getInfo()

    printTitle("Time measurements")

    for i, bazooka in enumerate(bazookaList):
        bazooka['timeBazooka'].getInfo()


def angleInformation(s):
    return f"Measurement for \u03b1 = {round(degrees(s), 2)}\u00b0"


if __name__ == "__main__":
    main()
