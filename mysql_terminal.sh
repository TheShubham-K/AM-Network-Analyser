#!/bin/bash
DIRNAME=$(basename "$PWD")
sudo docker run -it --network ${DIRNAME}_default --rm mysql mysql -ham-db -uroot -p
