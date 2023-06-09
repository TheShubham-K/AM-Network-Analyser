## DOCKER VERSIONS

- Docker version: 20.10.5, build 55c4c88
- Docker Compose version: 1.28.6, build 5db8d86f

## WHAT THIS APP DOES

- It basically generates some HTTP/S traffic, analyzes it, inserts relevant data(Outgoing port + destination IP) into a MySQL database.
- The data is then exported through a MySQL exporter into a Prometheus scraper which offers relevant metrics(e.g. inserts)
- There is also a Grafana dashboard which is not yet properly configured.

## STEP BY STEP TESTING GUIDE

- From the root folder of the project, `run docker-compose build`, then `docker-compose up`(it will take a bit until the db is ready to accept connections)
- Should you wish to check the MySQL database, run the mysql_terminal.sh script with the password password which will set up a root connection to the db(you might have to give it execute rights)
- Once logged in, write the commands USE network_data; then SELECT * FROM traffic; which should show the table data
- Should you wish to check the exported data manually, you can access the exporter at localhost:9104
- The Prometheus front-end can be accessed at localhost:9090 where you can graph different values from the exporter(e.g. mysql_global_status_commands_total{command="insert"})
- By default, the program listens on ports 80 and 443(HTTP & HTTPS), but you can add more by editing the docker-compose file(am-analyzer service, PORTS environment variable)
- I added some HTTPS sources to test the multi-port parsing, but I removed them before sending the archive so that it works as you intended

## PYTHON PARSER

- My approach is to create a python subprocess(tcpdump port 80 -nn), then process the lines as they come from the subprocess. Regarding the actual extraction of the addresses & ports, I make use of the fact that all messages have the same layout and use a series of finds on the line in order to create isolate where the addresses are located. A more elegant solution would have been a regex, but this should do for a smaller project like this one.
- I chose python as its ease of use made it perfect for a project like this

## FOLDER LAYOUT
app

- contains resources necessary for the first container(Dockerfile for building the image, the several scripts, the sources)

db

- contains an init.sql file that will be create a new database & table when the database container is up and running

prometheus

- contains the .yml configuration file for the Prometheus scraper

## DOCKER COMPOSE CONTAINERS LAYOUT

- The app consists of 4 containers put together with Docker Compose:

am-analyzer (created from the am-network-analyzer custom image)

- The image is derived from the python one(which itself is based on Debian IIRC), on top of which I added tcpdump and mysql-connector-python
- Contains the producer shell script along with the sources and the python parser
- It also contains a shell script which runs the python parser in the foreground and the producer script in the background
- Has several environment variables set that deal with the MySQL connection
- On startup, the container will exit with an error and restart itself several times until the database is ready to accept connections

am-db (created from the mysql image)

- Contains the MySQL database and has a db named network_data with a table named traffic with the following layout:
  time_recorded(DATETIME) ip_address(destination ip, VARCHAR) port(the port on the host machine from where the request to the HTTP port was sent, INT)
- I provided a shell script for easily launching a terminal with a root connection to the database(mysql_terminal.sh)(password: password - security 101 right there)
- Exposes port 3306

am-db-exporter (created from the prom/mysqld-exporter image)

- Contains the Prometheus MySQL exporter which connects to the database and exposes port 9104
- Has an environment variable set for the connection to the database
- Can be accessed from localhost:9104 should you wish to check the exported data manually

am-prometheus (created from the prom/prometheus image)

- Contains the Prometheus scraper and exposes port 9090
- By default, it scrapes every 5s(can be modified in the config file from the prometheus folder)
- Can be accessed from localhost:9090
