Flask+Postgres
==============
psql -h localhost -U hjh -d blog

利用flask建表
------------
创建一个flaskwork.py
``` py
@app.cli.command()
def create_db():
    """创建数据表"""
    db.create_all()
```

利用flask创建用户
---------------
``` py
@app.cli.command()
def init_user():
    """创建用户"""
    u = User(username='admin', password='admin')
    db.session.add(u)
    db.session.commit()
```

执行
----
```
export FLASK_APP=flaskwork.py
flask
```
*查看执行命令*

测试
===
pytest -s -v -k test_xxx xxx.py