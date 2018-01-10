def get_node_name(node):
  return node[1]['name']


def get_node_type(node):
  return node[0]


def is_leaf_node(node):
  if type(node) is list:
    return True
  else:
    return False
