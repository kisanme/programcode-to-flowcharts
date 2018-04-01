import lib.phplex as phplex
import lib.phpparse as yacc_parse
import translator.toflow as tf
from itertools import tee, islice, chain
import pprint
import classifier.classifier as classifier
import drawer.drawer as fld

drawable_stack = []
drawing_node = 0


# Parsing invocation
def parse_through_lex(file_path):
  data = open(file_path, 'r').read()
  phplex.full_lexer.input(data)
  return phplex.full_lexer


'''
  Level-1 parsing: No inner-blocks are parsed.
'''
def recursive_shallow_parsing(nodes):
  if nodes is False:
    return

  # If the node is a leaf node, will return the node itself.
  if tf.is_leaf_node(nodes):
    return nodes
  else:
    for node in nodes:
      if not tf.is_leaf_node(node):
        if isinstance(node, tuple):
          # recursive_shallow_parsing(tf.get_child(tf.get_node_type(node), tf.get_node_attributes(node)))
          node_type = tf.identify_translate_to(node)
          drawable = (node_type, node)
          if drawable[0] is not False:
            drawable_stack.append(drawable)
          processed_node = recursive_shallow_parsing(tf.get_nodes(tf.get_node_attributes(node)))
          # drawable_stack.append((tf.get_node_typ(node), recursive_shallow_parsing(tf.get_nodes(node))))
        else:
          processed_node = recursive_shallow_parsing(tf.get_nodes(node))
          if processed_node is not None:
            # This is buggy: It only checks the very first node item, say the first statement of the block
            drawable = tf.identify_translate_to(processed_node[0]), processed_node
            # drawable_stack.append(drawable)
            # if drawable[0] is not False:
            #   drawable_stack.append(drawable)
            # print('drawable (from list):', drawable_stack)
          # #print('processed_node list:', processed_node)
          # drawable_stack.append((tf.get_node_type(node), recursive_shallow_parsing(tf.get_nodes(node))))
  return nodes


'''
  Parsing the class item and re-assigning the first node of the node lists
  Assumption, the first method in the class is the method that needs the flowchart drawn
'''
def pre_parse(nodes):
  if nodes[0] == 'Class':
    nodes = nodes[1]
    nodes = nodes['nodes'][0]
    return nodes


'''
  Shallow parsing for AST
  Will only parse the code by main constructs
  In-depth parsing for each constructs should be done using deep_parse(root_node)
'''
def shallow_parse(nodes):
  nodes = pre_parse(nodes)

  if nodes is False:
    return
  nodes = recursive_shallow_parsing(nodes)
  return nodes


# Parsing
lexemes = parse_through_lex('./php_test_files/BasicClass.php')
parser = yacc_parse.make_parser()
parsed_ast = yacc_parse.run_parser(parser, open('./php_test_files/BasicClass.php', 'r'), True, False)

ast_processed = []
for statement in parsed_ast:
  if hasattr(statement, 'generic'):
    statement = statement.generic()
    ast_processed = statement

# pprint.pprint(ast_processed)
print()
# rp_parsed = recursive_shallow_parsing(ast_processed)
rp_parsed = shallow_parse(ast_processed)

print('')
print('Drawable stack: ')
pprint.pprint(drawable_stack)


drawing_item = 1;


'''
  IO node manipulation.
  The node will be obtained after shallow parsing.
'''
def io_node(node):
  shape = tf.identify_translate_to(node)
  output_text = tf.get_processed_text_from_node(node)
  print(shape)
  print(output_text)
  return shape, output_text 


'''
  Decision node manipulation.
  The node will be obtained after shallow parsing.
'''
def decision_node(node):
  decision_output = ('add_decision', {
    'condition': '',
    'true': [],
    'false': [],
    'elseif': [],
  })
  node_type = tf.get_node_type(node)
  if node_type in ['If', 'ElseIf']:
    else_items = []
    elif_container = []

    expression = tf.get_node_values(node[1], 'expr')
    true_items = tf.get_node_values(tf.get_node_values(node[1], 'node')[1], 'nodes')
    # Else-if could be not present in the logic
    if tf.get_node_values(node[1], 'elseifs'):
      elif_container = tf.get_node_values(node[1], 'elseifs')
    # Else could be not present in the logic
    if tf.get_node_values(node[1], 'else_'):
      else_items = tf.get_node_values(tf.get_node_values(node[1], 'else_')[1]['node'][1], 'nodes')

    # print('EXPRESSION: ')
    shape_text = tf.get_processed_text_from_node(expression)
    mapped_drawer = tf.identify_translate_to(expression)
    decision_output[1]['condition'] = shape_text
    # print(mapped_drawer)
    # print(shape_text)

    # print()
    for i in true_items:
      # print('true item: ')
      mapped_drawer = tf.identify_translate_to(i)
      shape_text = tf.get_processed_text_from_node(i)
      decision_output[1]['true'].append((mapped_drawer, shape_text))
      # print(mapped_drawer)
      # print(shape_text)

    '''
      Recursively calls the same method to generate the else-if block
    '''
    for el_if in elif_container:
      rd_built = decision_node(el_if)
      decision_output[1]['false'].append(rd_built)

    # print()
    for i in else_items:
      # print('else item: ')
      mapped_drawer = tf.identify_translate_to(i)
      shape_text = tf.get_processed_text_from_node(i)
      decision_output[1]['false'].append((mapped_drawer, shape_text))
      # print(mapped_drawer)
      # print(shape_text)

    # print('ELSE IF CONTAINER')
    # pprint.pprint(elif_container)

    '''
      Recursively calls the same method to generate the else-if block
    for el_if in elif_container:
      rd_built = decision_node(el_if)
      decision_output[1]['elseif'].append(rd_built)
    '''

  # TODO - WHILE Node evaluation
  elif node_type == 'While':
    print('While Node')
  return decision_output


'''
  Process node manipulation.
  The node will be obtained after shallow parsing.
'''
def process_node(node):
  shape = tf.identify_translate_to(node)
  # print(shape)
  output_text = tf.get_processed_text_from_node(node)
  # print(output_text)
  return shape, output_text


'''
  Parsing in-depth (recursive parsing)
  The root_node is obtained after shallow parsing.
'''
def deep_parse(root_node, node_type='add_process'):
  drawing_item = ()
  if node_type == 'add_io':
    # print("IO")
    shape, output_text = io_node(root_node)
    drawing_item = shape, output_text
    # print(shape, output_text)
  elif node_type == 'add_process':
    # print("Process")
    shape, output_text = process_node(root_node)
    drawing_item = shape, output_text
    # print(shape, output_text)
  elif node_type == 'add_decision':
    # print('DECISION')
    shape = decision_node(root_node)
    drawing_item = shape
    # pprint.pprint(shape)
    # print(shape, output_text)
  return drawing_item


def condition_drawing(drawing_shape, res_draw, item, count):
  el_if_cond_id = 0
  last_el_if_id = 0
  last_el_if_ids = []
  num_el_if_items = 0
  num_else_items = 0

  drawing_shape(item[1]['condition'], count)
  # Connect the condition node to the previous statement
  cond_id = count
  res_draw.connect(count-1, cond_id)

  # True block
  if len(item[1]['true']) > 0:
    # Maintaining a new counter for true statements
    t_count = 1110
    # Connect the if condition with an edge to the true block
    res_draw.connect(cond_id, t_count, 'True')
    for t_item in item[1]['true']:
      drawing_shape = getattr(res_draw, t_item[0])
      drawing_shape(t_item[1], t_count)
      # if item[1]['true']
      if t_count > 1110:
        res_draw.connect(t_count-1, t_count)
      t_count += 1
    # The last node of else block connects to the rest of 
    #   the statement outside the else block
    res_draw.connect(t_count-1, count+1)

  # Else block
  if len(item[1]['false']) > 0:
    # Maintaining a new counter for else statements
    f_count = 10000
    # Connect the if condition with an edge to the else block
    res_draw.connect(cond_id, f_count, 'False')

    for e_item in item[1]['false']:

      # ELSE-IF statement
      if e_item[0] == 'add_decision':

        # Checking whether have their been any other else-if block prior
        # If so, then the next else-if block
        if el_if_cond_id > 0:
          res_draw.connect(el_if_cond_id, f_count, 'False')

        # Drawing else-if condional diamond
        el_if_cond_id = f_count

        print('ELIF condition id', el_if_cond_id)
        drawing_shape = getattr(res_draw, e_item[0])
        drawing_shape(e_item[1]['condition'], el_if_cond_id)

        # Drawing ELSE-IF conditionally true block
        if len(e_item[1]['true']) > 0:

          print('Connection count', f_count+1, el_if_cond_id)
          # Connect 'true' edge to the 1st node within the block
          res_draw.connect(el_if_cond_id, f_count+1, 'True')
          num_el_if_items += 1

          for e_if_item in e_item[1]['true']:
            f_count += 1
            drawing_shape = getattr(res_draw, e_if_item[0])
            drawing_shape(e_if_item[1], f_count)
            print('THANI block', f_count)

            # Connect the nodes within a single else-if block
            if (el_if_cond_id != f_count-1):
              res_draw.connect(f_count-1, f_count)
            
            # Increment the number of ELSE-IF statements
            num_el_if_items += 1
              
          # List of tail nodes of ELSE-IF block
          last_el_if_ids.append(f_count)
        last_el_if_id = f_count

      # Else statements
      else:
        num_else_items += 1

        # Drawing the connection between last ELSE-IF condition to the ELSE block
        if el_if_cond_id > 0 and f_count - last_el_if_id == 1:
          res_draw.connect(el_if_cond_id, f_count, 'False')
        
        # Drawing each ELSE statement and the corresponding connection
        drawing_shape = getattr(res_draw, e_item[0])
        drawing_shape(e_item[1], f_count)

        # Condition for min bound:  and f_count <= (10000-1 + num_el_if_items + num_else_items)
        # Draw connections within the ELSE statements
        if f_count > el_if_cond_id and f_count > max(*last_el_if_ids)+1:
          res_draw.connect(f_count-1, f_count)

      f_count += 1

    '''
    # The last node of else block connects to the rest of 
    #   the statement outside the else block
    '''
    # Connect every ending node of ELSE-IF block to the rest of outer sphere
    [res_draw.connect(lif_node_id, count+1) for lif_node_id in last_el_if_ids]

    res_draw.connect(f_count-1, count+1)


def draw_results(draw_list):
  count = 1
  res_draw = fld.Drawer(None)
  res_draw.initialize_drawing()
  cond_id = count
  for item in draw_list:
    print('Drawing list')
    drawing_shape = getattr(res_draw, item[0])
    if isinstance(item[1], str):
      drawing_shape(item[1], count)
      if (count-1 != cond_id):
        res_draw.connect(count-1, count)
      print(count, item)
    
    '''
      Blocked statement - Complex statements
      Like If-else-elseif and While
    '''
    if isinstance(item[1], dict):
      cond_id = count
      condition_drawing(drawing_shape, res_draw, item, cond_id)

      
      print('Complex block')
    count += 1
  res_draw.end(count-1)
  res_draw.get_drawing().write('../outputs/final_drawing.dot')
  res_draw.get_drawing().draw('../outputs/final_drawing.png', prog='dot')

    # res_draw.add_process('$counter = 0;')



# Deep parse the shallow parsed tree
drawing_list = []
for node in drawable_stack:
  n_type = node[0]
  print()
  print()
  drawing_list.append(deep_parse(node[1], n_type))

print('FINAL DRAWING:')
pprint.pprint(drawing_list)
draw_results(drawing_list)

# Test some imperative style coding
# yacc_parse.run_parser(parser, open('./php_test_files/Imperative.php', 'r'), False, False)


# Customized Drawing
# ==================

'''
chart = None
x = fld.Drawer(chart)
for previous, drawing_entity, nxt in previous_and_next(drawable_stack):
  if drawing_entity[0] is False:
    continue

  if isinstance(drawing_entity, tuple):
    # print(drawing_entity)
    if drawing_entity[1][0] == 'If':
      item_name = 'If (1== 2)'
      getattr(x, drawing_entity[0])(item_name)
      # Drawing Else part
      if drawing_entity[1][1]['else_'][1]['node'][1]['nodes']:
        print('else', drawing_entity[1][1]['else_'][1]['node'][1]['nodes'][0][1]['nodes'])
        inner_item = 'echo ("' + drawing_entity[1][1]['else_'][1]['node'][1]['nodes'][0][1]['nodes'][0] + '")'
        getattr(x, 'add_process')(inner_item)
        x.connect('If (1== 2)', inner_item, 'False')
        x.end(inner_item)
      # print('item value', tf.get_node_values(drawing_entity[1]))
      # print(drawing_entity[1][1]['expr'])
    else:
      item_name = 'echo ("' + drawing_entity[1][1]['nodes'][0] + '")'
      # print('item', drawing_entity[1])
      # print('item value', tf.get_node_values(drawing_entity[1]))
      getattr(x, drawing_entity[0])(item_name)

  # Connection logic
  if previous is not None:
    if item_name == 'Hi':
      x.connect('If (1== 2)', item_name, 'False')
    x.connect('If (1== 2)', item_name, 'True')

  else:
    x.connect('Start', item_name)
  if nxt is None:
    x.end(item_name)
    # #print(drawing_entity[1][1]['nodes'])
  # drawing_entity[1][1]['nodes'] = 'an if condition'
'''

# Drawing stuffs
# ==============

# x.get_drawing().write('../outputs/x.dot')
# x.get_drawing().draw('../outputs/x.png', prog='circo')
#
# # While loop drawing
# while_drawer = fld.Drawer(None)
# while_drawer.connect('Start', '$counter = 0;')
# while_drawer.add_process('$counter = 0;')
# while_drawer.connect('$counter = 0;', '$counter < 100')
# while_drawer.add_decision('$counter < 100')
# while_drawer.connect('$counter < 100', '$some_array[] = $counter;', 'True')
# while_drawer.add_process('$some_array[] = $counter;')
# while_drawer.connect('$some_array[] = $counter;', '$counter ++;')
# while_drawer.add_process('$counter ++;')
# while_drawer.connect('$counter ++;', '$counter < 100')
# while_drawer.end('$counter < 100', 'False')
# while_drawer.get_drawing().draw('outputs/while.png', prog='circo')
#
# print('hello world')