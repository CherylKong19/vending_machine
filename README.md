
# Vending machine application

This repository contains main files to build a **microservice** application in **Docker**. 
This is an application for hand sanitizer and masks vending machines.

The transactions are stored to allow the following:
- Analysis of the data to prepare the number of hand sanitizer and masks needed in different locations
- fulfilment staff to reload the hand sanitizer or masks when low availability of stock
- Customer to view so that they will not do transaction but not getting the product
### Pre-requisite
1. Docker is installed
2. Zookeeper, Kafka and MySQL is installed and configured

### Before running the code
1. Change all needed information like hostname, database information, user information and etc.

### Build Docker image for each service
1. Direct to each folder except deployment
2. Run command `docker build –t <folder_name>:latest .`

### Run Docker Images with Docker Compose  
1. Direct to deployment folder
2. Run command `docker-compose up –d`

### To run individual images
1. Run command `docker run -d -p <port>:<port> <img_name>`

### To stop and remove containers, 
1. Run command `docker-compose down`

### Jenkins shared library
- [Jenkins Repo](https://github.com/CherylKong19/ass3_ci_functions)
