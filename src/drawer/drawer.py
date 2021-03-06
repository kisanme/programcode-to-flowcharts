# ------------------------------
# A drawer for drawing flowchart diagrams.
#
# Both the nodes and edges of the diagram can be chained and called
# by adding a prefix to their names.
#
# @author Nasik Shafeek <nasik2ms@gmail.com>
# ------------------------------

import pygraphviz


class Drawer(object):

  def __init__(self, gr, debug=False):
    self.debug = debug
    self.gr = gr  # type: pygraphviz.AGraph
    self.initialize_drawing()

  def initialize_drawing(self):
    self.gr = pygraphviz.AGraph(directed=True, rankdir='TB', )
    self.gr.node_attr['shape'] = 'rectangle'
    self.gr.add_node(0, label='Start', shape='ellipse')

  def add_process(self, process_name, nid):
    process_name = (process_name + ' : ' + str(nid)) if self.debug == True else process_name
    self.gr.add_node(nid, label=process_name, shape='rectangle')

  def add_io(self, io_name, nid):
    io_name = (io_name + ' : ' + str(nid)) if self.debug == True else io_name
    self.gr.add_node(nid, label=io_name, shape='parallelogram')

  def add_decision(self, decision_name, nid):
    decision_name = (str(decision_name) + ' : ' + str(nid)) if self.debug == True else decision_name
    self.gr.add_node(nid, label=decision_name, shape='diamond')

  def connect(self, from_node, to_node, connect_name=''):
    self.gr.add_edge(from_node, to_node, label=connect_name)

  def end(self, from_node, edge_name=''):
    end_name = 'End'
    self.gr.add_node(end_name, shape='ellipse')
    self.connect(from_node, end_name, edge_name)
  
  def get_node(self, nid):
    return self.gr.get_node(nid)
  
  def get_nodes(self):
    return self.gr.nodes()

  def get_drawing(self):
    return self.gr
