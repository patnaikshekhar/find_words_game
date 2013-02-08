# -*- coding: utf-8 *-*
import time


class Timer():
    """
        This is the timer class used to keep time
    """
    def __init__(self, minutes):
        self.minutes = minutes

    def start(self):
        """
            This function starts the timer
        """
        if self.minutes:
            self.startTime = time.time()
            self.endTime = time.time() + (self.minutes * 60)

    def getTimeLeft(self):
        """
            This function gets the time left on the timer
        """
        if self.startTime and self.endTime:
            totalSecondsLeft = self.endTime - time.time()

            if totalSecondsLeft < 0:
                return None

            minutesLeft = int(totalSecondsLeft / 60)
            secondsLeft = int(totalSecondsLeft % 60)

            # Create formated return string
            returnString = ""

            if minutesLeft <= 0:
                returnString = "00"
            elif minutesLeft < 10:
                returnString = "0" + str(minutesLeft)
            else:
                returnString = str(minutesLeft)

            returnString = returnString + " : "

            if secondsLeft <= 0:
                returnString = returnString + "00"
            elif secondsLeft < 10:
                returnString = returnString + "0" + str(secondsLeft)
            else:
                returnString = returnString + str(secondsLeft)

            return returnString

        return 0
