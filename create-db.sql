CREATE DATABASE collection;
CREATE USER myuser WITH PASSWORD 'pass-here';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE collection TO myuser;
ALTER USER myuser CREATEDB;
