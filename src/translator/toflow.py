# Or rather check for the attribute 'nodes' and traverse
traverse_node_types = {
  'Block',
  'ListAssignment',
  'Global',
  'Static',
  'Echo',
  'Unset',
  'Try',
  'Catch',
  'Finally',
  'Function',
  'Method',
  'Closure',
  'Class',
  'Trait',
  'ClassConstants',
  'ClassVariables',
  'Interface',
  'IsSet',
  'Array',
  'Switch',
  'Case',
  'Default',
  'ConstantDeclarations'
}

fields = {
  'If': 'expr',
  'Else': 'expr',
  'Echo': 'nodes',
  'BinaryOp': ['op', 'left', 'right']
}

def get_node_name(node):
  return get_node_attributes(node)['name']


def get_node_type(node):
  if isinstance(node, str):
    return node
  if not node[0]:
    return
  return node[0]


# TODO
# This needs modification,
# node_type should work based on a dictionary of key value pairs
def get_child(node_type, node):
  if node.get(node_type):
    return node[node_type]


def get_nodes(node):
  if node.get('nodes'):
    return node['nodes']
  elif node.get('node'):
    return node['node']
  elif node.get('else_'):
    return node.get['else_']
  return False


def get_node_attributes(node):
  if not node[1]:
    return
  return node[1]


def get_node_values(node):
  response = {}
  if isinstance(node, tuple):
    node_field = fields[get_node_type(node)]

    if isinstance(node_field, list):
      for field in node_field:
        response[field] = node[1][field]
        # print('response within loop', field, response[field])
        get_node_values(response[field])
      # print('response', response)
    else:
      # print('response non instance', node[1][node_field])
      get_node_values(node[1][node_field])
  else:
    # print('response none', node)
    return node



def is_leaf_node(node):
  if isinstance(node, str):
    return True
  else:
    return False


def is_decision(node):
  decisions = [
    'If',
    'Else'
    'ElseIf',
    'While',
    'DoWhile',
    'For',
    'ForEach',
    # 'Switch',
    'Case'
  ]

  if get_node_type(node) in decisions:
    return True
  return False


def is_io(node):
  input_outputs = [
    'Constant',
    'Variable',
    'StaticVariable',
    'LexicalVariable',
    'FormalParameter',
    'Parameter'
  ]

  if get_node_type(node) in input_outputs:
    return True
  return False


def is_process(node_type):
  processes = [
    'Assignment',
    'ListAssignment',
    'Echo',
    'Print',
    'Unset',
    'Try',
    'Catch',
    'Finally',
    'Throw',
    'FunctionCall',
    'MethodCall',
    'StaticMethodCall'
  ]

  if get_node_type(node_type) in processes:
    return True
  return False


def identify_translate_to(node_type):
  print('identify_translate_to', node_type)
  if is_decision(node_type):
    return 'add_decision'
  elif is_process(node_type):
    return 'add_process'
  elif is_io(node_type):
    return 'add_io'
  else:
    return False
