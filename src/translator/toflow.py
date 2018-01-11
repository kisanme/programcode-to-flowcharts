# Or rather check for the attribute 'nodes' and traverse
traverse_node_types = [
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
]


def get_node_name(node):
  return get_node_attributes(node)['name']


def get_node_type(node):
  if not node[0]:
    return
  return node[0]


def get_nodes(node):
  if node.get('nodes'):
    return node['nodes']
  return False


def get_node_attributes(node):
  if not node[1]:
    return
  return node[1]


def is_leaf_node(node):
  if isinstance(node, str):
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


def identify_translate_to(node):
  print(node)
  if is_decision(node):
    return 'add_decision'
  elif is_process(node):
    return 'add_process'
  elif is_io(node):
    return 'add_io'
  else:
    return False
