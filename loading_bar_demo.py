import time


def console_bar(currentPercentage, barLength):
    currentBarPercentage = int((currentPercentage / 100) * barLength)
    remainingBarPercentage = barLength - currentBarPercentage
    bar = "[" + currentBarPercentage * "#" + remainingBarPercentage * "-" + "]"
    print("\r" + bar, end="", flush=True)
    time.sleep(0.1)

bar_length = 20

for i in range(0, 101):
    console_bar(currentPercentage=i, barLength=bar_length)