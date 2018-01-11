def get_node_name(node):
  return node[1]['name']


def get_node_type(node):
  return node[0]


def is_leaf_node(node):
  if type(node) is list:
    return True
  else:
    return False


def is_decision(node):
  decisions = [
    'If',
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


def is_process(node):
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

  if get_node_type(node) in processes:
    return True
  return False
