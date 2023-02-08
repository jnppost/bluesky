""" BlueSky plugin template. The text you put here will be visible
    in BlueSky as the description of your plugin. """
# Import the global bluesky objects. Uncomment the ones you need
import bluesky as bs
from bluesky import core, stack, traf, settings, navdb, sim, scr, tools


def init_plugin():
    maps_loaded = []

    

    def maptoggle_func(fname):
        t_offset = sim.simt
        # Read the scenario file
        # readscn(fname, pcall_arglst, t_offset)
        # if fname.strip('del_').upper() in tbar_lst:
        #     fname = 'maps/' + fname
        # else:
        #     fname = 'maps/' + fname
        fname = '../plugins/LVNL_data/scenario/Maps/' + fname
        insidx = 0
        instime = sim.simt

        try:
            for (cmdtime, cmdline) in stack.simstack.readscn(fname):

                # Time offset correction
                cmdtime += t_offset

                if not stack.stackbase.Stack.scentime or cmdtime >= stack.stackbase.Stack.scentime[-1]:
                    stack.stackbase.Stack.scentime.append(cmdtime)
                    stack.stackbase.Stack.scencmd.append(cmdline)
                else:
                    if cmdtime > instime:
                        insidx, instime = next(
                            ((j, t) for j, t in enumerate(stack.stackbase.Stack.scentime) if t >= cmdtime),
                            (len(stack.stackbase.Stack.scentime), stack.stackbase.Stack.scentime[-1]),
                        )
                    stack.stackbase.Stack.scentime.insert(insidx, cmdtime)
                    stack.stackbase.Stack.scencmd.insert(insidx, cmdline)
                    insidx += 1

            # stack any commands that are already due
            stack.stackbase.checkscen()
        except FileNotFoundError as e:
            return False, f"maptoggle: File not found'{e.filename}'"

    @stack.command(brief="map filename")
    def map(fname):
        if fname in maps_loaded:
            maps_loaded.remove(fname)
            fname = 'del_' + fname
            maptoggle_func(fname)
        else:
            maps_loaded.append(fname)
            maptoggle_func(fname)

    config = {
        # The name of your plugin
        'plugin_name':     'MAPTOGGLE',
        # The type of this plugin.
        'plugin_type':     'sim'
        }

    return config


