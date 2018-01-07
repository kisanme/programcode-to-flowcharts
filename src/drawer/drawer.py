import pygraphviz


class Drawer(object):

  def __init__(self, gr):
    self.gr = gr # type: pygraphviz.AGraph
    self.initialize_drawing()

  def initialize_drawing(self):
    self.gr = pygraphviz.AGraph(directed=True, strict=True, rankdir='LR')

  def add_process(self, process_name):
    self.gr.add_node(process_name, shape='rectangle')

  def add_io(self, io_name):
    self.gr.add_node(io_name, shape='parallelogram')

  def connect(self, from_node, to_node):
    self.gr.add_edge(from_node, to_node)

  def get_drawing(self):
    return self.gr
