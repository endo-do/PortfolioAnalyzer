CREATE TABLE exchange (
    exchangeid INT PRIMARY KEY AUTO_INCREMENT,
    exchangename VARCHAR(255) NOT NULL UNIQUE,
    region INT NOT NULL,
    foreign key (region) references region(regionid)
)