from pathlib import Path

__all__ = [
    'PROJECT_DIR',
    'PLUGINS_DIR',
]

PROJECT_DIR = Path(__file__).parent.parent.absolute()
PLUGINS_DIR = f'{PROJECT_DIR}/app/plugins'
