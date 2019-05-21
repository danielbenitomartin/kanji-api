CREATE DATABASE users_prod;
CREATE DATABASE users_dev;
CREATE DATABASE users_test;
CREATE DATABASE jmdict;
CREATE USER jmdictdb WITH encrypted password 'your_password';
CREATE USER jmdictdbv WITH encrypted password 'your_password';
GRANT all privileges ON database jmdict to jmdictdb;
GRANT all privileges ON database jmdict to jmdictdbv;
