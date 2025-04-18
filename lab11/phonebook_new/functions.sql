CREATE OR REPLACE FUNCTION add_entry(
  uname VARCHAR,
  ph    VARCHAR
) RETURNS VOID AS $$
BEGIN
  INSERT INTO phonebook_new(username, phone)
    VALUES (uname, ph)
    ON CONFLICT (username) DO NOTHING;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_phone_entry(
  uname      VARCHAR,
  new_phone  VARCHAR
) RETURNS VOID AS $$
BEGIN
  UPDATE phonebook_new
    SET phone = new_phone
    WHERE username = uname;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_username_entry(
  old_uname  VARCHAR,
  new_uname  VARCHAR
) RETURNS VOID AS $$
BEGIN
  UPDATE phonebook_new
    SET username = new_uname
    WHERE username = old_uname;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_entry(
  uname VARCHAR
) RETURNS VOID AS $$
BEGIN
  DELETE FROM phonebook_new
    WHERE username = uname;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_entries()
  RETURNS TABLE(username VARCHAR, phone VARCHAR) AS $$
BEGIN
  RETURN QUERY
    SELECT phonebook_new.username,
           phonebook_new.phone
      FROM phonebook_new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION find_by_username(
  pattern VARCHAR
) RETURNS TABLE(username VARCHAR, phone VARCHAR) AS $$
BEGIN
  RETURN QUERY
    SELECT phonebook_new.username,
           phonebook_new.phone
      FROM phonebook_new
     WHERE phonebook_new.username ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION find_by_phone(
  pattern VARCHAR
) RETURNS TABLE(username VARCHAR, phone VARCHAR) AS $$
BEGIN
  RETURN QUERY
    SELECT phonebook_new.username,
           phonebook_new.phone
      FROM phonebook_new
     WHERE phonebook_new.phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
