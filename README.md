# 资源预约系统

一个使用 Python 和 MySQL 构建的本地公共资源预约系统，配备了基于 tkinter 的简易图形界面。

## 功能特性

- **用户管理**：支持两种类型的用户——管理员和普通用户（学生/教师）。
- **资源管理**：按类别、位置、名称和可用状态管理共享资源。
- **预约管理**：支持按小时的时间段预约、冲突检测、个人预约记录查询及固定课程排程。
- **分类查询**：管理员可查看用户详细信息；普通用户只能查看资源占用情况以保障隐私。
- **数据库**：基于 MySQL 后端，采用关系表设计。
- **图形界面**：使用 tkinter 实现的简易界面。

## 项目结构

```
ResourceReservationSystem/
│
├── README.md               # 项目概览
├── requirements.txt        # 项目依赖
├── db/
│   ├── schema.sql          # 数据库创建所需的 SQL 结构脚本
│   └── queries.sql         # 用于增删改查操作的 SQL 语句
├── src/
│   ├── main.py             # 主程序入口，含图形界面
│   ├── database.py         # 数据库连接与操作
│   ├── user.py             # 用户管理逻辑
│   ├── resource.py         # 资源管理逻辑
│   └── reservation.py      # 预约管理逻辑
└── docs/
    └── ER_Diagram.md       # 实体-关系图（ER 图）
```

## 环境搭建

1. 安装依赖：`pip install -r requirements.txt`
2. 设置 MySQL 数据库：
   - 登录 MySQL：`mysql -u root -p`
   - 运行结构脚本以创建数据库和数据表：`source db/schema.sql`
   - 或者，也可以将 `db/schema.sql` 文件中的内容复制粘贴至 MySQL 命令行中执行。
3. 运行应用程序：`python src/main.py`

## 数据库设计

请参考 `docs/ER_Diagram.md` 文件，了解 ER 图及表之间的关系。

## SQL 操作

数据库管理所需的 SQL 语句位于 `db/queries.sql` 文件中。
