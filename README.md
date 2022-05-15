# PawMed
A project in the course "Databases Systems and Applications" in 6th semester of computer science.

Instruction for running PostgreSql database with Django:
1. Install Docker and optionally Docker Desktop
2. Install latest PostgreSql official image with: 
```
docker pull postgres
```
3. Run database image with Docker Desktop or using
```
docker run --name pawmed -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:latest 
```
4. Connect to database using preferred admin tool
4. Run model creation script form db-scripts directory
