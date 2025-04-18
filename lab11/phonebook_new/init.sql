DROP TABLE IF EXISTS phonebook_new;

CREATE TABLE phonebook_new (
  username VARCHAR(50) PRIMARY KEY,
  phone    VARCHAR(20) NOT NULL
);
