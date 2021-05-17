DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  q_text TEXT NOT NULL,
  code TEXT NOT NULL,
  testcase TEXT NOT NULL
);

-- CREATE TABLE testcases (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   q_id INTEGER NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (q_id) REFERENCES question (id)
-- );