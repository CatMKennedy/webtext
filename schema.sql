drop table if exists entries;
create table entries (
  id integer  primary key autoincrement,
  title text not null,
  author text not null,
  genre text not null,
  corpusID text not null,
  fileID text not null,
  url text not null
);
