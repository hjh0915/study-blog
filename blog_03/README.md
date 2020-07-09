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
