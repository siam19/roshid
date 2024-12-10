import importlib
import logging
import pkgutil

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self, package):
        if not hasattr(package, '__path__'):
            logging.error(f"Package {package.__name__} has no __path__ attribute")
            return
        
        for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
            try:
                # Construct the full module name
                module_name = f"{package.__name__}.{name}"
                logging.info(f"Module name: {module_name}")
                # Import the module
                module = importlib.import_module(module_name)

                # Check if the module has 'DeliveryServicePlugin'
                if hasattr(module, 'DeliveryServicePlugin'):
                    plugin_class = module.DeliveryServicePlugin
                    init_params = module.DeliveryServiceInitParams()

                    # Instantiate the plugin and store it
                    self.plugins[name] = plugin_class(init_params)
                    logging.info(f"Successfully loaded plugin: {name}")
            except ImportError as e:
                logging.error(f"Failed to import plugin '{name}': {e}")
            except Exception as e:
                logging.error(f"Error loading plugin '{name}': {e}", exc_info=True)