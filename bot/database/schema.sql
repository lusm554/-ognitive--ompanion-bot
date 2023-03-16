CREATE TABLE IF NOT EXISTS USERS (
  user_id      SERIAL PRIMARY KEY,
  telegram_id  INT,
  username     VARCHAR,
  nickname     VARCHAR,
  phone_number VARCHAR,
  created_at   TIMESTAMP,
  updated_at   TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_index on USERS (telegram_id, username);

CREATE TABLE IF NOT EXISTS BOARDS (
  board_id      SERIAL PRIMARY KEY,
  owner_id      INT,
  board_name    VARCHAR,
  created_at   TIMESTAMP,
  updated_at   TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES USERS (user_id)
);
CREATE INDEX IF NOT EXISTS boards_index on BOARDS (owner_id);

CREATE TABLE IF NOT EXISTS BOARD_PERMISSIONS (
  board_permission_id        SERIAL PRIMARY KEY,
  board_id                   INT,
  granted_permission_user_id INT,
  created_at                 TIMESTAMP,
  updated_at                 TIMESTAMP,
  FOREIGN KEY (board_id) REFERENCES BOARDS (board_id),
  FOREIGN KEY (granted_permission_user_id) REFERENCES USERS (user_id)
);
CREATE INDEX IF NOT EXISTS board_permissions_index on BOARD_PERMISSIONS (board_id, granted_permission_user_id);

CREATE TABLE IF NOT EXISTS LISTS (
  list_id      SERIAL PRIMARY KEY,
  board_id     INT,
  owner_id     INT,
  list_name    VARCHAR,
  created_at   TIMESTAMP,
  updated_at   TIMESTAMP,
  FOREIGN KEY (board_id) REFERENCES BOARDS (board_id),
  FOREIGN KEY (owner_id) REFERENCES USERS (user_id)
);
CREATE INDEX IF NOT EXISTS lists_index on LISTS (board_id);


CREATE TABLE IF NOT EXISTS TASKS (
  task_id       SERIAL PRIMARY KEY,
  list_id       INT,
  owner_id      INT,
  assigned_to   INT,
  task_name     VARCHAR,
  "description" VARCHAR,
  due_dt        TIMESTAMP,
  created_at    TIMESTAMP,
  updated_at    TIMESTAMP,
  FOREIGN KEY (list_id) REFERENCES LISTS (list_id),
  FOREIGN KEY (owner_id) REFERENCES USERS (user_id),
  FOREIGN KEY (assigned_to) REFERENCES USERS (user_id)
);
CREATE INDEX IF NOT EXISTS tasks_index on TASKS (list_id, owner_id, assigned_to);

SELECT table_name 
FROM information_schema.tables 
WHERE 
  table_schema = 'public';

