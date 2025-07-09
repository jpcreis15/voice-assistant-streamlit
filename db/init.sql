CREATE TABLE user_management (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  person_name VARCHAR(100),
  user_password VARCHAR(100) NOT NULL,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cookies (
  id SERIAL PRIMARY KEY,
  expiry_days INT NOT NULL,
  key_str VARCHAR(200) NOT NULL,
  name_cookie VARCHAR(200),
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE preauthorized (
  id SERIAL PRIMARY KEY,
  email VARCHAR(200) NOT NULL,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user_management (username, email, person_name, user_password)
VALUES ('admin', 'admin@gmail.com', 'Admin', '$2b$12$OX.eFPsSCrUzCdldwBqSguyWKY4F67XQhWgtwKZP/1.SdaYbWibtm');

INSERT INTO cookies (expiry_days, key_str, name_cookie)
VALUES (30, 'qwerty', 'voice_assistant_cookie');

INSERT INTO preauthorized (email)
VALUES ('admin@gmail.com');

