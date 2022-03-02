#!/bin/bash
echo Give me your secret key
read txt
echo SECRET_KEY=$txt > "../Clinic-with-Lab/.env"