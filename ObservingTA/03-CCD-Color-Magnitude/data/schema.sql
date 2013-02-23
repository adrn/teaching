drop table if exists filter;
create table filter (
  id integer primary key autoincrement,
  name string not null
);

create table wcs (
  id integer primary key autoincrement,
  image_filename string not null,
  wcs_filename string not null
);