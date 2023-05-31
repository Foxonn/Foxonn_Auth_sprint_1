import glob
from importlib.machinery import SourceFileLoader
from pathlib import Path

__all__ = [
    'loads_plugins',
]


def loads_plugins(path_to_plugins: str) -> None:
    for file in glob.glob(f'{path_to_plugins}/*/*_plugin.py'):
        module_name = Path(file).name[:-3]
        SourceFileLoader(module_name, file).load_module()
