import lib.phplex as phplex
import lib.phpparse as yacc_parse
import translator.toflow as tf
from itertools import tee, islice, chain
import pprint
import classifier.classifier as classifier
import drawer.drawer as fl_drawer

drawable_stack = []


# Parsing invocation
def parse_through_lex(file_path):
  data = open(file_path, 'r').read()
  phplex.full_lexer.input(data)
  return phplex.full_lexer


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


# Parsing the class item and re-assigning the first node of the node lists
# Assumption, the first method in the class is the method that needs the flowchart drawn
def pre_parse(nodes):
  if nodes[0] == 'Class':
    nodes = nodes[1]
    nodes = nodes['nodes'][0]
    return nodes


# Shallow parsing for AST
# Will only parse the code by main constructs
# In-depth parsing for each constructs should be done using deep_parse(root_node)
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


processed_drawables = {}
drawing_item = 1;


def io_node(node):
  node_type = tf.get_node_type(node)
  out = ''
  if node_type == 'Echo':
    # Echo output preparation can use the centralized method: tf.get_processed_text_from_node(node)
    item_type = tf.identify_translate_to(node)
    item = tf.get_node_values(node[1])
    out = 'echo ("' + tf.get_echo_text(item) + '")'
    print('ECHO TYPE: ', item_type)
    print('ECHO OUTPUT: ', out)
  return out


def decision_node(node):
  node_type = tf.get_node_type(node)
  if node_type == 'If':
    elif_items = []
    else_items = []

    expression = tf.get_node_values(node[1], 'expr')
    true_items = tf.get_node_values(tf.get_node_values(node[1], 'node')[1], 'nodes')
    # Else-if could be not present in the logic
    if tf.get_node_values(node[1], 'elseifs'):
      elif_items = tf.get_node_values(tf.get_node_values(tf.get_node_values(node[1], 'elseifs')[0][1]['node'], 'Block'), 'nodes')
    # Else could be not present in the logic
    if tf.get_node_values(node[1], 'else_'):
      else_items = tf.get_node_values(tf.get_node_values(node[1], 'else_')[1]['node'][1], 'nodes')

    print('EXPRESSION: ')
    # pprint.pprint(expression)
    shape_text = tf.get_processed_text_from_node(expression)
    print(shape_text)

    print()
    # pprint.pprint(true_items)
    for i in true_items:
      print('true item: ')
      mapped_drawer = tf.identify_translate_to(i)
      shape_text = tf.get_processed_text_from_node(i)
      print(mapped_drawer)
      print(shape_text)

    print()
    # pprint.pprint(else_items)
    for i in else_items:
      print('else item: ')
      mapped_drawer = tf.identify_translate_to(i)
      shape_text = tf.get_processed_text_from_node(i)
      print(mapped_drawer)
      print(shape_text)

    print()
    # pprint.pprint(elif_items)
    for i in elif_items:
      print('else if items: ')
      mapped_drawer = tf.identify_translate_to(i)
      shape_text = tf.get_processed_text_from_node(i)
      print(mapped_drawer)
      print(shape_text)
  elif node_type == 'While':
    print('While Node')


def deep_parse(root_node, node_type='add_process'):
  parse_val = ''
  if node_type == 'add_io':
    parse_val = (io_node(root_node))
  elif node_type == 'add_process':
    print("Process")
    # print(tf.get_node_type(root_node))
  elif node_type == 'add_decision':
    print('DECISION')
    decision_node(root_node)
  return root_node


# Deep parse the shallow parsed tree
for node in drawable_stack:
  n_type = node[0]
  print()
  print()
  deep_parse(node[1], n_type)


# Test some imperative style coding
# yacc_parse.run_parser(parser, open('./php_test_files/Imperative.php', 'r'), False, False)


# For accessing previous/next elements in for loops
def previous_and_next(some_iterable):
  prevs, items, nexts = tee(some_iterable, 3)
  prevs = chain([None], prevs)
  nexts = chain(islice(nexts, 1, None), [None])
  return zip(prevs, items, nexts)


# Customized Drawing
# ==================

'''
chart = None
x = fl_drawer.Drawer(chart)
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
# while_drawer = fl_drawer.Drawer(None)
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