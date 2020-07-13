创建角色数据库表
=============
create table roles(  
   id int NOT NULL,  
   default boolean,
   name varchar(100),
   permisstions int,
   PRIMARY KEY(id)  
);

创建实时数据库表
=============
create table follows(  
   follower_id int NOT NULL,  
   followed_id int NOT NULL,
   timestamps timestamp,
   PRIMARY KEY(follower_id, followed_id)  
);

ALTER TABLE users ADD location varchar(100);
ALTER TABLE users ADD about_me text;
ALTER TABLE users ADD member_since timestamp;
ALTER TABLE users ADD last_seen timestamp;
ALTER TABLE users ADD avater_hash varchar(50);
ALTER TABLE users ADD email varchar(50);
ALTER TABLE users ADD confirmed boolean;

创建传递数据库表
=============
create table posts(  
   id int NOT NULL,  
   author_id int,
   body text,
   body_html text,
   timestamps timestamp,
   PRIMARY KEY(id)  
);

创建评论数据库表
==============
create table comments(  
   id int NOT NULL,  
   author_id int,
   body text,
   body_html text,
   timestamps timestamp,
   disabled boolean,
   post_id int,
   PRIMARY KEY(id)    
);

insert into users (email) values (admin@qq.com),(娃哈哈@qq.com),(旺仔@qq.com);
ALTER TABLE roles DROP COLUMN permisstions;

admin    1234
旺仔      123456
娃哈哈    1234