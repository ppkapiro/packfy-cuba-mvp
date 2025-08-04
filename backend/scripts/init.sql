-- Create the database
CREATE DATABASE paqueteria;

-- Connect to the database
\c paqueteria;

-- Create necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "hstore";
