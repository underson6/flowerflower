DROP TABLE IF EXISTS cart;
CREATE TABLE cart (
session_id text,
product_id int,
count int,
update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

DROP TABLE IF EXISTS product;
create table product (
id int AUTO_INCREMENT,
name text not null,
detail text,
price int,
recommend boolean,
tag text,
order_start datetime,
order_end datetime,
image text,
regist_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
primary key (id));

insert into product (name, detail, price, recommend, image) values ("hoge", "hogehoge", 2000, 0, null);
insert into product (name, detail, price, recommend, image) values ("fuga", "fugafuga", 2000, 0, null);
insert into product (name, detail, price, recommend, image) values ("gaba", "gabagaba", 2000, 1, null);
insert into product (name, detail, price, recommend, image) values ("gaba", "gabagaba", 2000, 0, null);
insert into product (name, detail, price, recommend, image) values ("daba", "dabadaba", 2000, 0, null);
insert into product (name, detail, price, recommend, image) values ("gaba", "gabagaba", 2000, 1, "rose.jpg");

create table customer(
id int AUTO_INCREMENT,
name text not null,
address text not null,
email text not null,
credit text not null,
member int(1),
primary key (id));

# create table orders (
# id int AUTO_INCREMENT,
# customer_id int,
# amout int,
# order_date datetime
# );

# create table order_detail (
#  id int,
#  order_id int,
#  product_id int,
#  count int
# );
