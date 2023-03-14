-- CREATE TABLE graber (
  -- id INTEGER PRIMARY KEY,
  -- data TEXT,
  -- link TEXT
-- );

CREATE TABLE spider (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dt TEXT,
  link TEXT,
  title TEXT,
  html TEXT,
  hash_html TEXT,
  screenshot TEXT,
  version INTEGER
);
