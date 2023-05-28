import subprocess as sub;
import re
from datetime import datetime
import mysql.connector
import os

# Process the rows as they come from the tcpdump subprocess
# Parameters : the subprocess, the ports on which to parse on and the connection to the database to add the data to
def processRows(subprocess, ports, database):
    for row in iter(subprocess.stdout.readline, ''):
        # Convert the row to a string
        rowAsStr = str(row.rstrip().decode("utf-8"))
        # TO DO : ADD SUPPORT FOR IPV6
        if (rowAsStr.find("IP6") != -1):
            continue
    
        # Parse the time
        time = datetime.strptime(rowAsStr[:19], '%Y-%m-%d %H:%M:%S')
        timeStr = str(time)

        # Find the bounds of the IPs
        # A more elegant solution would have been a regex
        ipIndex1 = rowAsStr.index("IP")
        ipIndex2LowerBound = rowAsStr.index(">")
        IPWithPort = rowAsStr[ipIndex1 + len("IP") + 1 : ipIndex2LowerBound - 1]
        # Split the sender IP address(In order to get the IP & Port as separate values)
        spl = IPWithPort.split(".")
        IP1 = ".".join(spl[0:4])
        port1 = spl[4]

        # Only take the requests to(not from) the specified ports into account
        shouldSkip = False
        for port in ports: 
            if (port1 == port):
                shouldSkip = True
                break
        if (shouldSkip):
            continue

        # Split the destination IP address
        ipIndex2UpperBound = rowAsStr.index("Flags") - 2
        IP2WithPort = rowAsStr[ipIndex2LowerBound + 2 : ipIndex2UpperBound]
        spl = IP2WithPort.split(".")
        IP2 = ".".join(spl[0:4])

        # Insert the values into the MySQL database
        myCursor = database.cursor()
        sql = "insert into traffic(time_recorded, ip_address, port) VALUES(%s, %s, %s)"
        val = (timeStr[:19], IP2, port1)
        myCursor.execute(sql, val)
        database.commit()


def main():
    # Create the MySQL connection
    mydb = mysql.connector.connect(
        host=os.environ.get("HOST"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        database=os.environ.get("DB")
    )
    
    # Set the ports on which we will parse
    portCmd = os.environ.get("PORTS")
    ports = portCmd.split(" ")
    # Join the ports with port %port or
    portStr = " ".join("port %s or" %port for port in ports)
    # Remove the last or
    portStr = portStr[:len(portStr) - 2]

    # Start the tcpdump subprocess & process its output
    p = sub.Popen(('tcpdump', portStr, '-nn', '-tttt', '-l'), stdout = sub.PIPE)
    processRows(p, ports, mydb)

if (__name__ == "__main__"):
    main()

 