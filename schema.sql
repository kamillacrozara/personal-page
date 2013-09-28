drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  author text not null,
  date text not null,
  title text not null,
  text text not null
);