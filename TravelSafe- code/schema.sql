drop table if exists users;
create table users(
id integer not null primary key autoincrement,
p_num bigint(15) not null,
password varchar(50) not null
);
drop table if exists friends;
create table friends(
id integer not null primary key autoincrement,
p_num bigint(15) not null,
f_num bigint(15) not null
);
drop table if exists vehicle;
create table vehicle(
  id integer not null primary key autoincrement,
  data varchar(100) not null
  p_num bigint(15) not null
);
drop table if exists details;
create table details(
  id integer not null,
  plate varchar(100) not null
);

