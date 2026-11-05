import importlib
import pkgutil
import os

def load_plugins():
    """
    Scans the plugins directory and loads all modules that export
    a 'PLUGIN' dictionary or a 'PLUGINS' list.
    Returns a list of plugin dictionaries sorted by their row index.
    """
    plugins = []
    package_dir = os.path.dirname(__file__)
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        module = importlib.import_module(f"plugins.{module_name}")
        if hasattr(module, "PLUGIN"):
            plugins.append(module.PLUGIN)
        if hasattr(module, "PLUGINS"):
            plugins.extend(module.PLUGINS)
    return sorted(plugins, key=lambda p: p["row"])
