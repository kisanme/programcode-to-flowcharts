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


def x_get_node_values(node):
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
  elif isinstance(node, list):
    print("dictionary", type(node), node)
    return node
  else:
    # print('response none', node)
    return node


def get_node_values(node, key=''):
  if isinstance(node, dict):
    if not key == '':
      return node.get(key, None)
    return node.get('nodes', None)
  elif isinstance(node, tuple):
    if key == 'Block' and node[0] == 'Block':
      return node[1]
    else:
      return node
  else:
    return

# This is not the ideal way to test the leaf node.
# TODO - modify this to see how many elements are contained within the node to check whether its a leaf node
def is_leaf_node(node):
  if isinstance(node, (str, int)):
    return True
  elif len(node) == 1:
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
    'Echo',
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
  if is_decision(node_type):
    return 'add_decision'
  elif is_process(node_type):
    return 'add_process'
  elif is_io(node_type):
    return 'add_io'
  else:
    return False


def get_var_name(var_node):
  print(var_node)
  if isinstance(var_node, tuple):
    return var_node[1].get('name', '')
  elif isinstance(var_node, dict):
    return var_node.get('name', '')
  else:
    return None


def get_var_expression(var_node):
  if isinstance(var_node, tuple):
    return str(var_node[1].get('expr', None))
  elif isinstance(var_node, dict):
    return str(var_node.get('expr', None))
  else:
    return ''


def get_echo_text(echo_node):
  if isinstance(echo_node, list):
    return ' '.join(echo_node)


def get_function_name(function_call):
  if isinstance(function_call, dict):
    return function_call.get('name')
  return ''


def get_function_params(function_call):
  parameters = []
  # Obtained as a list of parameters
  if isinstance(function_call, list):
    for param in function_call:
      if isinstance(param, tuple):
        # A string or integer parameter would be identified here
        item = get_node_values(param[1], 'node')
        # In-case of a variable, we'd need to go into another level
        if isinstance(item, tuple) and item[0] == 'Variable':
          item = get_node_values(item[1], 'name')
        # In-case of a string parameter, it needs be reflected
        # Variables are strings too ;)
        if isinstance(item, str) and item[0] != "$":
          item = '"' + item + '"'
        # Appends to a list, which will consequently be used for join() method
        parameters.append((str(item)))
  return ', '.join(parameters)


def get_processed_text_from_node(node):
  output_text = ''
  if isinstance(node, tuple):
    if node[0] == 'Assignment':
      var_name = get_var_name(get_node_values(node[1], 'node'))
      var_value = get_var_expression(node)
      output_text = var_name + ' = ' + var_value
    elif node[0] == 'Echo':
      output_text = 'echo("' + get_echo_text(get_node_values(node[1], 'nodes')) + '")'
    elif node[0] == 'FunctionCall':
      func_name = get_function_name(node[1])
      output_text = func_name + '(' + get_function_params(get_node_values(node[1], 'params')) + ')'
  return output_text

