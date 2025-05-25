# create-flask-app

一个用于快速生成标准化Flask应用脚手架的命令行工具。

## 功能特性

- 生成符合Flask最佳实践的项目结构
- 支持多种项目模板（basic/minimal/api/advanced）
- 集成常用数据库支持（SQLite/PostgreSQL/MySQL）
- 可选的功能模块（用户认证、REST API、Admin界面等）
- 开发工具链配置（测试、代码格式化、类型检查等）
- Docker支持

## 安装

这个还不行。目前还在开发中，没有上传到


```bash
pip install create-flask-app
```

## 使用方法

```bash
create-flask-app myproject --template=basic --db=sqlite
```

更多使用说明请参考[文档](docs/README.md)。

## 开发

1. 克隆项目：

```bash
git clone https://github.com/teddyxiong53/create-flask-app.git
cd create-flask-app
```

2. 创建虚拟环境：

```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 安装开发依赖：

```bash
uv pip install -e .
```

## 许可证

MIT