from math import degrees, asin


class Measurement:
    def __init__(self, s, h, v0GuessList, distanceList, timeList, timeCorrectionList=None):
        self.s = s  # base range
        self.h = h  # y position of the back of the bazooka
        self.v0GuessList = v0GuessList
        self.distanceList = distanceList
        self.timeList = timeList
        self.timeCorrectionList = timeCorrectionList

    def getAngle(self, y0, l):
        return degrees(asin((y0 - self.h) / l))
