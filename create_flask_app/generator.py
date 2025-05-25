import os
import secrets
from pathlib import Path
from typing import Any, Dict, List
from .utils import ensure_directory, copy_template, echo_info

class FlaskAppGenerator:
    def __init__(self,
                 project_name: str,
                 template_type: str = 'basic',
                 database: str = 'none',
                 auth_enabled: bool = False,
                 admin_enabled: bool = False,
                 api_enabled: bool = False,
                 frontend_type: str = 'simple') -> None:
        """初始化Flask应用生成器。

        Args:
            project_name: 项目名称
            template_type: 模板类型（basic/minimal/api/advanced）
            database: 数据库类型（none/sqlite/postgresql/mysql）
            auth_enabled: 是否启用认证
            admin_enabled: 是否启用Admin界面
            api_enabled: 是否启用REST API
            frontend_type: 前端类型（none/simple/webpack）
        """
        self.project_name = project_name
        self.template_type = template_type
        self.database = database
        self.auth_enabled = auth_enabled
        self.admin_enabled = admin_enabled
        self.api_enabled = api_enabled
        self.frontend_type = frontend_type

        # 项目根目录
        self.project_dir = Path.cwd() / project_name
        # 模板目录
        self.template_dir = Path(__file__).parent / 'templates'

    def generate(self) -> None:
        """生成Flask应用项目。"""
        # 创建项目目录结构
        self._create_directory_structure()
        
        # 生成项目文件
        self._generate_app_files()
        self._generate_config_files()
        self._generate_test_files()
        self._generate_requirements()
        self._generate_docker_files()
        self._generate_docs()
        # 生成 WSGI 入口文件
        self._render_template('wsgi.py.j2',
                        self.project_dir / 'wsgi.py',
                        self._get_template_context())
    def _create_directory_structure(self) -> None:
        """创建项目目录结构。"""
        dirs = [
            self.project_dir / 'app' / 'models',
            self.project_dir / 'app' / 'templates',
            self.project_dir / 'app' / 'static',
            self.project_dir / 'app' / 'config',
            self.project_dir / 'tests',
            self.project_dir / 'requirements',
        ]

        for dir_path in dirs:
            ensure_directory(dir_path)
            (dir_path / '__init__.py').touch()

    def _generate_app_files(self) -> None:
        """生成应用核心文件。"""
        context = self._get_template_context()

        # 生成主应用文件
        self._render_template('app/__init__.py.j2',
                            self.project_dir / 'app' / '__init__.py',
                            context)
        
        # 生成路由文件
        self._render_template('app/routes.py.j2',
                            self.project_dir / 'app' / 'routes.py',
                            context)

        # 如果启用认证，生成认证相关文件
        if self.auth_enabled:
            self._render_template('app/auth.py.j2',
                                self.project_dir / 'app' / 'auth.py',
                                context)

        # 如果启用API，生成API相关文件
        if self.api_enabled:
            self._render_template('app/api.py.j2',
                                self.project_dir / 'app' / 'api.py',
                                context)
        
        # 生成模板文件
        template_files = [
            'base.html.j2',
            'index.html.j2',
            'dashboard.html.j2',
            'auth/login.html.j2',
            'auth/register.html.j2'
        ]
        for template_file in template_files:
            self._render_template(f'app/templates/{template_file}',
                                self.project_dir / 'app' / 'templates' / template_file.replace('.j2', ''),
                                context)

    def _generate_config_files(self) -> None:
        """生成配置文件。"""
        context = self._get_template_context()
        context['secret_key'] = secrets.token_hex(32)

        # 生成配置文件
        config_files = ['__init__.py', 'development.py', 'production.py', 'testing.py']
        for file in config_files:
            self._render_template(f'config/{file}.j2',
                                self.project_dir / 'app' / 'config' / file,
                                context)

        # 生成环境变量文件
        self._render_template('.env.j2',
                            self.project_dir / '.env',
                            context)

    def _generate_test_files(self) -> None:
        """生成测试文件。"""
        context = self._get_template_context()

        # 生成测试配置和基础测试用例
        self._render_template('tests/conftest.py.j2',
                            self.project_dir / 'tests' / 'conftest.py',
                            context)
        self._render_template('tests/test_basic.py.j2',
                            self.project_dir / 'tests' / 'test_basic.py',
                            context)

    def _generate_requirements(self) -> None:
        """生成依赖文件。"""
        context = self._get_template_context()

        # 生成基础和开发环境依赖文件
        self._render_template('requirements/base.txt.j2',
                            self.project_dir / 'requirements' / 'base.txt',
                            context)
        self._render_template('requirements/dev.txt.j2',
                            self.project_dir / 'requirements' / 'dev.txt',
                            context)

    def _generate_docker_files(self) -> None:
        """生成Docker相关文件。"""
        context = self._get_template_context()

        # 生成Dockerfile和docker-compose.yml
        self._render_template('Dockerfile.j2',
                            self.project_dir / 'Dockerfile',
                            context)
        self._render_template('docker-compose.yml.j2',
                            self.project_dir / 'docker-compose.yml',
                            context)

    def _generate_docs(self) -> None:
        """生成文档文件。"""
        context = self._get_template_context()

        # 生成README.md
        self._render_template('README.md.j2',
                            self.project_dir / 'README.md',
                            context)

    def _get_template_context(self) -> Dict[str, Any]:
        """获取模板渲染上下文。

        Returns:
            Dict[str, Any]: 模板上下文
        """
        return {
            'project_name': self.project_name,
            'template_type': self.template_type,
            'database': self.database,
            'auth_enabled': self.auth_enabled,
            'admin_enabled': self.admin_enabled,
            'api_enabled': self.api_enabled,
            'frontend_type': self.frontend_type,
        }

    def _render_template(self, template_path: str, output_path: Path,
                        context: Dict[str, Any]) -> None:
        """渲染模板文件。

        Args:
            template_path: 模板文件路径
            output_path: 输出文件路径
            context: 模板上下文
        """
        src = self.template_dir / template_path
        if not src.exists():
            echo_info(f"跳过不存在的模板文件: {template_path}")
            return

        copy_template(src, output_path, context)