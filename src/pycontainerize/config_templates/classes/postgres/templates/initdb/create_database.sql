CREATE EXTENSION IF NOT EXISTS dblink;
DO
$do$
BEGIN
   IF EXISTS (SELECT 1 FROM pg_database WHERE datname = '{{ app.db.postgres.name }}') THEN
      RAISE NOTICE 'Database already exists';
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE {{ app.db.postgres.name }}');
      ALTER DATABASE {{ app.db.postgres.name }} OWNER TO {{ app.db.postgres.user }};
   END IF;
END
$do$;
