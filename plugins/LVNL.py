""" BlueSky plugin template. The text you put here will be visible
    in BlueSky as the description of your plugin. """
# Import the global bluesky objects. Uncomment the ones you need
import bluesky as bs
from bluesky import core, stack, traf, settings, navdb, sim, scr, tools, plugins


def init_plugin():
    stack.stack("PLUGIN MAPTOGGLE")

    config = {
        # The name of your plugin
        'plugin_name':     'LVNL',
        # The type of this plugin.
        'plugin_type':     'sim'
        }

    return config


