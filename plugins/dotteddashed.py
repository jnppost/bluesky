""" BlueSky plugin template. The text you put here will be visible
    in BlueSky as the description of your plugin. """
import numpy as np
# Import the global bluesky objects. Uncomment the ones you need
from bluesky import stack, ui  #, settings, navdb, sim, scr, tools
from bluesky.ui.qtgl.glhelpers import gl, RenderObject, VertexArrayObject, ShaderSet
from bluesky.ui.qtgl.glpoly import POLY_SIZE

# Dotted lines pixel interval
interval_dotted = 3

# Dashed lines pixel interval
interval_dashed = 5

# Points size
point_size = 4

### Initialization function of your plugin. Do not change the name of this
### function, as it is the way BlueSky recognises this file as a plugin.
def init_plugin():
    ''' Plugin initialisation function. '''
    # Configuration parameters
    config = {
        # The name of your plugin
        'plugin_name':     'dotsdashes',

        # The type of this plugin.
        'plugin_type':     'gui',
        }

    # init_plugin() should always return a configuration dict.
    return config


### Entities in BlueSky are objects that are created only once (called singleton)
### which implement some traffic or other simulation functionality.
### To define an entity that ADDS functionality to BlueSky, create a class that
### inherits from bluesky.core.Entity.
### To replace existing functionality in BlueSky, inherit from the class that
### provides the original implementation (see for example the asas/eby plugin).
# class Dashed(RenderObject, layer=100):
#     ''' Example new render object for BlueSky. '''
#     def __init__(self, parent):
#         super().__init__(parent=parent)
#         self.alldashed = VertexArrayObject(gl.GL_LINES, shader_type='dashed')
#
#     def create(self):
#         self.alldashed.create(vertex=POLY_SIZE * 16, color=POLY_SIZE * 8)
#
#     def draw(self):
#         dashed_shader = ShaderSet.get_shader('dashed')
#         dashed_shader.bind()
#
#         gl.glUniform1f(dashed_shader.uniforms['dashSize'].loc, float(interval_dashed))
#         gl.glUniform1f(dashed_shader.uniforms['gapSize'].loc, float(interval_dashed))
#         self.alldashed.draw()
#
#     def update_poly_data_dashed(self, name, coordinates=None, color=None):
#         self.dashed = dict()
#         if coordinates is not None:
#             self.dashed.pop(name, None)
#
#             newdata = np.array(coordinates, dtype=np.float32)
#             contourbuf = np.array(newdata, dtype=np.float32)
#             fillbuf = np.array([], dtype=np.float32)
#
#             # Define color buffer for outline
#             defclr = tuple(color or palette.polys) + (255,)
#             colorbuf = np.array(len(contourbuf) // 2 * defclr, dtype=np.uint8)
#
#             self.dashed[name] = (contourbuf, fillbuf, colorbuf)
#
#
#     # You can create new stack commands with the stack.command decorator.
#     # By default, the stack command name is set to the function name.
#     # The default argument type is a case-sensitive word. You can indicate different
#     # types using argument annotations. This is done in the below function:
#     # - The color argument returns three integer values (r, g, b), which is why the
#     #   starred notation is used here.
#     @stack.command
#     def DASHEDLINE(self, name, lat1, lon1, lat2, lon2):
#         ''' Set the color of my example shape. '''
#         self.update_poly_data_dashed
#

### Entities in BlueSky are objects that are created only once (called singleton)
### which implement some traffic or other simulation functionality.
### To define an entity that ADDS functionality to BlueSky, create a class that
### inherits from bluesky.core.Entity.
### To replace existing functionality in BlueSky, inherit from the class that
### provides the original implementation (see for example the asas/eby plugin).
@stack.command
def mycolor(self, *colour: 'colour'):
    ''' Set the color of my example shape. '''
    MyVisual()

class MyVisual(RenderObject, layer=100):
    ''' Example new render object for BlueSky. '''
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.shape = VertexArrayObject(gl.GL_TRIANGLE_FAN)
        self.shape.create()
        self.shape.draw()

    def create(self):
        vertices = np.array([52, 5, 52, 4, 54, 4, 54, 5], dtype = np.float32)
        self.shape.create(vertex=vertices, color=(255, 0, 0))

    def draw(self):
        self.shaderset.set_vertex_scale_type(self.shaderset.VERTEX_IS_LATLON)
        self.shape.draw()

    # You can create new stack commands with the stack.command decorator.
    # By default, the stack command name is set to the function name.
    # The default argument type is a case-sensitive word. You can indicate different
    # types using argument annotations. This is done in the below function:
    # - The color argument returns three integer values (r, g, b), which is why the
    #   starred notation is used here.


