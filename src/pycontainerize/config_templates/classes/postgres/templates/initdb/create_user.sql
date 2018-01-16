DO 'DECLARE num_users INTEGER;
BEGIN
   SELECT count(*)
    INTO num_users
    FROM pg_user WHERE  usename = ''{{ app.db.postgres.user }}'';

    IF num_users = 0 THEN
        CREATE ROLE {{ app.db.postgres.user }} LOGIN PASSWORD ''{{ app.db.postgres.password }}'';
    END IF;
END';
