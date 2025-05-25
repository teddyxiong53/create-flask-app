import os
import re
import click
from pathlib import Path
from typing import Optional
from .generator import FlaskAppGenerator
from .utils import validate_project_name, echo_info, echo_error, echo_success

@click.command()
@click.argument('project_name')
@click.option('--template', type=click.Choice(['basic', 'minimal', 'api', 'advanced']),
              default='basic', help='项目模板类型')
@click.option('--db', type=click.Choice(['none', 'sqlite', 'postgresql', 'mysql']),
              default='none', help='数据库类型')
@click.option('--with-auth/--no-auth', default=False, help='是否包含用户认证模块')
@click.option('--with-admin/--no-admin', default=False, help='是否包含Admin界面')
@click.option('--with-api/--no-api', default=False, help='是否包含REST API支持')
@click.option('--frontend', type=click.Choice(['none', 'simple', 'webpack']),
              default='simple', help='前端集成类型')
def main(project_name: str,
        template: str,
        db: str,
        with_auth: bool,
        with_admin: bool,
        with_api: bool,
        frontend: str) -> None:
    """创建一个新的Flask应用项目。

    PROJECT_NAME 是新项目的名称，将用作项目目录名。
    """
    try:
        # 验证项目名称
        if not validate_project_name(project_name):
            echo_error(f"无效的项目名称: {project_name}")
            echo_info("项目名称必须符合Python包命名规范")
            return

        # 检查目标目录
        project_dir = Path.cwd() / project_name
        if project_dir.exists():
            echo_error(f"目录已存在: {project_dir}")
            return

        # 创建项目生成器实例
        generator = FlaskAppGenerator(
            project_name=project_name,
            template_type=template,
            database=db,
            auth_enabled=with_auth,
            admin_enabled=with_admin,
            api_enabled=with_api,
            frontend_type=frontend
        )

        # 生成项目
        echo_info("正在创建Flask应用...")
        generator.generate()

        # 显示成功信息
        echo_success(f"\n✨ Flask应用创建成功！")
        echo_info(f"\n进入项目目录并启动开发服务器：")
        echo_info(f"  cd {project_name}")
        echo_info(f"  python -m venv .venv")
        echo_info(f"  source .venv/bin/activate  # Windows: .venv\\Scripts\\activate")
        echo_info(f"  pip install -r requirements/dev.txt")
        echo_info(f"  flask run --debug")

    except Exception as e:
        echo_error(f"创建项目时出错: {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    main()