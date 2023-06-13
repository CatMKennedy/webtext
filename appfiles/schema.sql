drop table if exists user;
drop table if exists entries;

create table user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

create table entries (
  id integer  primary key autoincrement,
  title text not null,
  author text not null,
  genre text not null,
  corpusID text not null,
  fileID text not null,
  url text not null
);
