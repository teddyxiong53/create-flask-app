import re
import click
from typing import Any
from pathlib import Path
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)

def validate_project_name(name: str) -> bool:
    """验证项目名称是否符合Python包命名规范。

    Args:
        name: 项目名称

    Returns:
        bool: 是否合法
    """
    if not name:
        return False
    
    # Python包名规范：只能包含字母、数字和下划线，且不能以数字开头
    pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    return bool(pattern.match(name))

def echo_info(message: str) -> None:
    """输出信息消息。

    Args:
        message: 要输出的消息
    """
    click.echo(f"{Fore.BLUE}ℹ {Style.RESET_ALL}{message}")

def echo_success(message: str) -> None:
    """输出成功消息。

    Args:
        message: 要输出的消息
    """
    click.echo(f"{Fore.GREEN}✓ {Style.RESET_ALL}{message}")

def echo_error(message: str) -> None:
    """输出错误消息。

    Args:
        message: 要输出的消息
    """
    click.echo(f"{Fore.RED}✗ {Style.RESET_ALL}{message}", err=True)

def ensure_directory(path: Path) -> None:
    """确保目录存在，如果不存在则创建。

    Args:
        path: 目录路径
    """
    path.mkdir(parents=True, exist_ok=True)

def copy_template(src: Path, dst: Path, context: dict[str, Any]) -> None:
    """复制并渲染模板文件。

    Args:
        src: 源文件路径
        dst: 目标文件路径
        context: 模板渲染上下文
    """
    from jinja2 import Environment, FileSystemLoader
    
    # 创建目标目录
    ensure_directory(dst.parent)
    
    # 如果是二进制文件，直接复制
    if src.suffix in ('.ico', '.png', '.jpg', '.gif'):
        import shutil
        shutil.copy2(src, dst)
        return
    
    # 渲染模板文件
    env = Environment(loader=FileSystemLoader(str(src.parent)))
    template = env.get_template(src.name)
    content = template.render(**context)
    
    # 写入目标文件
    dst.write_text(content)