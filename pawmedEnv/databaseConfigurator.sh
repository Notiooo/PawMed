#!/bin/bash
echo Give me your database name: 
read name
echo DATABASE_NAME=$name > "../PawMed/.env"
echo Give me your database host:
read host
echo DATABASE_HOST=$host >> "../PawMed/.env"
echo Give me your database port: 
read port
echo DATABASE_PORT=$port >> "../PawMed/.env"
echo Give me your database user: 
read user
echo DATABASE_USER=$user >> "../PawMed/.env"
echo Give me your database password: 
read password
echo DATABASE_PASSWORD=$password >> "../PawMed/.env"