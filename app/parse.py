import subprocess as sub;
import re
from datetime import datetime
import mysql.connector
import os

# Process the rows as they come from the tcpdump subprocess
# Parameters : the subprocess and the connection to the database to add the data to
def processRows(subprocess, database):
    for row in iter(subprocess.stdout.readline, ''):
        # Convert the row to a string
        rowAsStr = str(row.rstrip().decode("utf-8"))

        # TO DO : ADD SUPPORT FOR IPV6
        if (rowAsStr.find("IP6") != -1):
            continue

        # Parse the time
        time = datetime.strptime(rowAsStr[:15], '%H:%M:%S.%f')
        timeStr = str(time)

        # Find the bounds of the IPs
        # A more elegant solution would have been a regex
        ipIndex1 = rowAsStr.index("IP")
        ipIndex2LowerBound = rowAsStr.index(">")
        IPWithPort = rowAsStr[ipIndex1 + len("IP") + 1 : ipIndex2LowerBound - 1]

        # Split the IP address(In order to get the IP & Port as separate values)
        spl = IPWithPort.split(".")

        # Insert the values into the MySQL database
        myCursor = database.cursor()
        sql = "insert into traffic(time_recorded, ip_address, port) VALUES(%s, %s, %s)"
        val = ((str(time))[11:19], ".".join(spl[0:4]), spl[4])
        myCursor.execute(sql, val)
        database.commit()


def main():
    print("HOST: " + os.environ.get("HOST"))
    # Create the MySQL connection
    mydb = mysql.connector.connect(
        host=os.environ.get("HOST"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        database=os.environ.get("DB")
    )
    # Start the tcpdump subprocess & process its output
    p = sub.Popen(('tcpdump', 'port 80', '-nn', '-l'), stdout = sub.PIPE)
    processRows(p, mydb)

if (__name__ == "__main__"):
    main()

 