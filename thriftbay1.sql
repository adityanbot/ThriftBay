CREATE database thriftbay;
USE thriftbay;
CREATE TABLE userdata(
    email VARCHAR(100) NOT NULL PRIMARY KEY UNIQUE,
    password VARCHAR(255) NOT NULL);
insert into userdata values("shreyassajith@gmail.com","testing");
insert into userdata values("akshatk@gmail.com","testing2");
    
    