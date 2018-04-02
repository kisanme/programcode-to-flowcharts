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
    elif (key == 'left' or key == 'right') and node[0] == 'Variable':
      return node[1]['name']
    else:
      return node[1][key]
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
    'Case',
    'BinaryOp'

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
    'StaticMethodCall',
    'PostIncDecOp',
    'PreIncDecOp'
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
  if isinstance(var_node, tuple):
    var_name = var_node[1].get('name', '')
    '''
      When the assignment is of an array item
      e.g: $x[] = 1; $x[1] = 23;
    '''
    if var_node[0] == 'ArrayOffset':
      var_name = get_var_name(get_node_values(var_node[1], 'node'))
      var_name += '['
      if get_node_values(var_node[1], 'expr') is not None:
        var_name += str(get_node_values(var_node[1], 'expr'))
      var_name += ']'
    return var_name
  elif isinstance(var_node, dict):
    return var_node.get('name', '')
  else:
    return None


def get_method_call(var_node):
  exp = get_object_name(var_node[1])
  exp += '->'
  exp += get_object_method(var_node[1])
  exp += '('
  exp += get_function_params(var_node[1]['params'])
  exp += ')'
  return exp


def get_new_object(var_node):
  exp = 'new '
  exp += get_object_method(var_node[1])
  exp += '('
  exp += get_function_params(var_node[1]['params'])
  exp += ')'
  return exp


def get_function_call(var_node):
  exp = get_function_name(var_node[1])
  exp += '('
  exp += get_function_params(var_node[1]['params'])
  exp += ')'
  return exp


# Returns the variable RHS value
#   @params var_node is the variable assignment node itself
# e.g: $hi = $hello->world();
def get_var_expression(var_node):
  if isinstance(var_node, tuple):
    print('variable expression node', var_node)
    exp = var_node[1].get('expr', None)

    '''
      If the assigning value is a method call
      e.g $hi = $hello->world();
    '''
    if (exp is None) and var_node[0] == 'MethodCall':
      exp = get_method_call(var_node)

    ''' 
      If the assigning value is a new object creation
      e.g: $hi = new Carbon();
    '''
    if isinstance(exp, tuple) and exp[0] == 'New':
      exp = get_new_object(exp)

    ''' 
      If the assigning value is a function call
      e.g: $hi = toToHell('as');
    '''
    if isinstance(exp, tuple) and exp[0] == 'FunctionCall':
      exp = get_function_call(exp)


    ''' 
      Get the variable name of the RHS
      e.g: $hi = $x;
    '''
    if var_node[0] == 'Variable':
      exp = get_node_values(var_node, 'name')

    '''
      Recursive call is necessary to identify items on the RHS like a Method Call
      e.g: $hi = $hello->sayHello();
    '''
    if isinstance(exp, tuple) and not (exp[0] == 'New'):
      exp = get_var_expression(exp)

    return str(exp)
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


def get_object_name(method_call):
  if isinstance(method_call, dict):
    obj = method_call.get('node')
    return get_node_values(obj, 'name')
  return ''


def get_object_method(method_call):
  if isinstance(method_call, dict):
    obj = method_call.get('name')
    params = get_function_params(method_call)
    return obj + params
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


# Returns binary value of whether the comparison operator is
def is_composite_operator(node):
  composite_operators = ['&&', '||', 'and', 'or', 'xor']
  if isinstance(node, tuple):
    # If the input is like: ('BinaryOp', {'op': '==', 'left': 1, 'right': 2})
    if node[1]['op'] in composite_operators:
      return True
  elif isinstance(node, dict):
    # If the input is like: {'op': '==', 'left': 1, 'right': 2}
    if node['op'] in composite_operators:
      return True
  return False


# Recursively evaluates binary operation of
#   if and elseif and while condition blocks
def recursive_binaryop_parse(node, out_text):
  non_recursive_bops = [
    'Variable',
    'IsSet',
    'Empty'
  ]

  # If the node isn't a tuple
  # eg: 1, 2, $x, $y
  # Returns the passed out_text as it is
  if not isinstance(node, tuple):
    return out_text

  # When special set of functions are used within the if expression
  # eg: isset($x) or empty($x)
  # returns the processed output text within this block
  if isinstance(node, tuple) and (node[0] in non_recursive_bops):
    if node[0] == 'IsSet':
      within_params = get_node_values(node[1], 'nodes')
      return 'isset(' + str(get_node_values(within_params[0][1], 'name')) + ')'
    if node[0] == 'Empty':
      within_params = get_node_values(node[1], 'expr')
      return 'empty(' + str(get_node_values(within_params[1], 'name')) + ')'
    return out_text

  # When the node under evaluation isn't composite
  # This transform the conditional clauses into strings of conditional clauses
  # Returns the output text of non-recursive constructs
  # e.g Returns 1 == 2, 1 >= 2
  if not is_composite_operator(node):
    l_operand = get_node_values(node, 'left')
    operator = get_node_values(node, 'op')
    r_operand = get_node_values(node, 'right')
    if isinstance(l_operand, tuple):
      l_operand = get_node_values(l_operand, 'name')
    if isinstance(r_operand, tuple):
      r_operand = get_node_values(r_operand, 'name')
    out_text = str(l_operand) + str(operator) + str(r_operand)
    return out_text

  # Recursive callee block
  # Uses left and right recursions to construct the ultimate if conditional expression
  # returns $x == 2 && 2 >= 1 || isset($x)
  if isinstance(node, tuple) and node[0] == 'BinaryOp':
    for n_item in node[1]:
      if not n_item == 'op':
        out_text = recursive_binaryop_parse(node[1]['left'], out_text) + ' ' + str(node[1]['op']) + ' ' + recursive_binaryop_parse(node[1]['right'], out_text) + ' '

  return out_text


def get_processed_text_from_node(node):
  output_text = ''
  if isinstance(node, tuple):
    if node[0] == 'Assignment':
      var_name = get_var_name(get_node_values(node[1], 'node'))
      var_value = get_var_expression(node)
      if isinstance(var_value, tuple):
        var_value = get_processed_text_from_node(var_value)
      output_text = var_name + ' = ' + var_value
    elif node[0] == 'Echo':
      output_text = 'echo("' + get_echo_text(get_node_values(node[1], 'nodes')) + '")'
    elif node[0] == 'FunctionCall':
      func_name = get_function_name(node[1])
      output_text = func_name + '(' + get_function_params(get_node_values(node[1], 'params')) + ')'
    elif node[0] == 'MethodCall':
      output_text = get_object_name(node[1])
      output_text += '->'
      output_text += get_object_method(node[1])
      output_text += '('
      output_text += get_function_params(node[1]['params'])
      output_text += ')'
    elif node[0] == 'StaticMethodCall':
      output_text = get_node_values(node[1], 'class_')
      output_text += '::'
      output_text += get_object_method(node[1])
      output_text += '('
      output_text += get_function_params(node[1]['params'])
      output_text += ')'
    elif node[0] == 'BinaryOp':
      output_text = 'if ( ' + str(recursive_binaryop_parse(node, '')) + ' )'
    elif node[0] == 'PreIncDecOp':
      operator = get_node_values(node[1], 'op')
      output_text = str(operator) + get_var_expression(node)
    elif node[0] == 'PostIncDecOp':
      operator = get_node_values(node[1], 'op')
      output_text =  get_var_expression(node) + str(operator)
  return output_text

