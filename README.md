就算有很方便的QQ作人与人间的互相联系，但是我还是享受自己创造这种联系的载体的成就感。
<h3>工程开源地址：</h3>

<h3>使用方法</h3>
1、文件内容：

<img class="alignnone size-medium wp-image-84" src="http://lanceliang2018.xyz/wp-content/uploads/1-300x139.jpg" alt="" width="300" height="139" />

database.db    和用户设置有关的数据库

entries.db    储存聊天记录的数据库

db_init.py    对数据库清空and初始化(debug)

db_list.py    列出数据库的所有内容(debug)

database.py    处理数据库有关操作

sever.py    服务器

templates/    Html的模板

2、开启服务器：

Linux：screen python3 sever.py    或者    python3 sever.py &amp;    (会有回显)

Windows：python sever.py
