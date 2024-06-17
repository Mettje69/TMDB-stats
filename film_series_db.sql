CREATE DATABASE film_series_db;

USE film_series_db;

CREATE TABLE films (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    release_date DATE,
    genre VARCHAR(100)
);

CREATE TABLE series (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    release_date DATE,
    genre VARCHAR(100),
    seasons INT
);

CREATE TABLE statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    film_id INT,
    series_id INT,
    date DATE,
    views INT,
    likes INT,
    dislikes INT,
    FOREIGN KEY (film_id) REFERENCES films(id),
    FOREIGN KEY (series_id) REFERENCES series(id)
);
