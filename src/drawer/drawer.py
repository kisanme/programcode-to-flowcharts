import pygraphviz


class Drawer(object):

  def __init__(self, gr):
    self.gr = gr # type: pygraphviz.AGraph
    self.initialize_drawing()

  def initialize_drawing(self):
    self.gr = pygraphviz.AGraph(directed=True, strict=True, rankdir='LR')
    self.gr.node_attr['shape'] = 'rectangle'
    self.gr.add_node('Start', shape='ellipse')

  def add_process(self, process_name):
    self.gr.add_node(process_name, shape='rectangle')

  def add_io(self, io_name):
    self.gr.add_node(io_name, shape='parallelogram')

  def add_decision(self, decision_name):
    self.gr.add_node(decision_name, shape='diamond')

  def connect(self, from_node, to_node, connect_name=''):
    self.gr.add_edge(from_node, to_node, label=connect_name)

  def end(self, from_node):
    end_name = 'End'
    self.gr.add_node(end_name, shape='ellipse')
    self.connect(from_node, end_name)

  def get_drawing(self):
    return self.gr
