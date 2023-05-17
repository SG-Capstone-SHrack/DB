CREATE TABLE members (
    id VARCHAR(20) NOT NULL,
    password VARCHAR(256) NOT NULL,
    name VARCHAR(50) NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
	birthdate DATE NOT NULL,
    height INT NOT NULL,
    weight INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id)
);

CREATE TABLE exercise (
	exercise_code INT NOT NULL AUTO_INCREMENT,
    exercise_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (exercise_code)
);

CREATE TABLE exercise_log (
	exercise_log_num INT NOT NULL AUTO_INCREMENT,
    id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    exercise_code INT NOT NULL,
	mass INT DEFAULT NULL,
    count INT NOT NULL,
    PRIMARY KEY (exercise_log_num),
    FOREIGN KEY (id) REFERENCES members(id),
    FOREIGN KEY (exercise_code) REFERENCES exercise(exercise_code),
    INDEX (id)
);