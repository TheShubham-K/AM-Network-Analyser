import subprocess as sub;
import re
from datetime import datetime

p = sub.Popen(('tcpdump', 'port 80', '-nn', '-l'), stdout = sub.PIPE)
for row in iter(p.stdout.readline, ''):
    # Convert the row to a string
    rowAsStr = str(row.rstrip().decode("utf-8"))
    # TO DO : ADD SUPPORT FOR IPV6
    if (rowAsStr.find("IP6") != -1):
        continue

    time = datetime.strptime(rowAsStr[:15], '%H:%M:%S.%f')
    timeStr = str(time)
    # Find the bounds of the IPs
    # A more elegant solution would have been a regex
    ipIndex1 = rowAsStr.index("IP")

    ipIndex2LowerBound = rowAsStr.index(">")
    ipIndex2UpperBound = rowAsStr.index("Flags")
    timeStamp = timeStr[11:]
    IP1 = rowAsStr[ipIndex1 + len("IP") + 1 : ipIndex2LowerBound - 1]
    IP2 = rowAsStr[ipIndex2LowerBound + 2 : ipIndex2UpperBound - 2]
    print(rowAsStr)
    print("Timestamp: " + timeStr[11:])
    print("IP1: " + IP1)
    port = (IP1.split("."))[4]
    print("Port: " + port)
 