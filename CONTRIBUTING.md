# Contribution Guide

- Find or create an issue on the repository addressing the change being made
- Fork the repository and create a branch
-

# Checklist

- The scope of each commit should be small so the impact of the change is clear.
- The commit summary should state the change and the message should be descriptive enough so a human readable CHANGELOG can be easily produced from the text.
- Sign off on all commits
- 

# Docker for Development

## MySQL

Start the container.

```
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -p 3306 mysql
```

Create the database.

```
docker exec -it mysql mysql --user=root --password=root < tests/input/chinook_mysql.sql > /dev/null
```

## PostgreSQL

Start the container.

```
docker run --name postgres -e POSTGRES_PASSWORD=root -p 5432 postgres
```

Create the database.

```
docker exec -it postgres psql -U postgres -d chinook -c 'create database chinook'
docker exec -it postgres psql -U postgres chinook < tests/input/chinook_postgresql.sql
```

## MongoDB

Currently there is no simple way to use a container for Mongo since the database must be restored from a directory of files that aren't available to the container.
