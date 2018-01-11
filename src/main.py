import lib.phplex as phplex
import lib.phpparse as yacc_parse
import translator.toflow as toflow
import pprint
import classifier.classifier as classifier
import drawer.drawer as fl_drawer

drawable_stack = []


# Parsing invocation
def parse_through_lex(file_path):
  data = open(file_path, 'r').read()
  phplex.full_lexer.input(data)
  return phplex.full_lexer


def recursive_parsing(nodes):
  if nodes is False:
    return

  # print('inside the recursive parser')
  if toflow.is_leaf_node(nodes):
    # print('leaf node', nodes)
    return nodes
  else:
    for node in nodes:
      if not toflow.is_leaf_node(node):
        print('none leaf node:', node)
        print()
        if isinstance(node, tuple):
          print('tuple item')
          # recursive_parsing(toflow.get_child(toflow.get_node_type(node), toflow.get_node_attributes(node)))
          drawable = (toflow.identify_translate_to(node[0]), node)
          if drawable[0] is not False:
            drawable_stack.append(drawable)
          print('drawable:', drawable_stack)
          processed_node = recursive_parsing(toflow.get_nodes(toflow.get_node_attributes(node)))
          # drawable_stack.append((toflow.get_node_typ(node), recursive_parsing(toflow.get_nodes(node))))
          # print('processed_node:', processed_node)
        else:
          print('list or dict or other item')
          processed_node = recursive_parsing(toflow.get_nodes(node))
          if processed_node is not None:
            drawable = toflow.identify_translate_to(processed_node[0]), processed_node
            # if drawable[0] is not False:
            #   drawable_stack.append(drawable)
            print('drawable (from list):', drawable_stack)
          # print('processed_node list:', processed_node)
          # drawable_stack.append((toflow.get_node_type(node), recursive_parsing(toflow.get_nodes(node))))

  return nodes


# print()
# print(drawable_stack)

# Parsing
lexemes = parse_through_lex('./php_test_files/BasicClass.php')
parser = yacc_parse.make_parser()
parsed_ast = yacc_parse.run_parser(parser, open('./php_test_files/BasicClass.php', 'r'), True, False)

ast_processed = []
for statement in parsed_ast:
  if hasattr(statement, 'generic'):
    statement = statement.generic()
    ast_processed = statement
    # pprint.pprint(statement)
    # print(toflow.get_node_name(statement))
  # if hasattr(statement, 'nodes'):
  #   print("HI")
  #   statement.generic()
  # pprint.pprint(statement)
  # print(toflow.get_node_name(statement))
  # print(toflow.get_node_type(statement))
  for item in statement:
    # pprint.pprint(item)
    if type(item) is dict and item['nodes']:
      # Has children nodes
      print()
      # pprint.pprint(toflow.get_nodes(item))
      # for node in toflow.get_nodes(item):
      #   pprint.pprint(toflow.get_nodes(toflow.get_node_attributes(node)))
      # print(toflow.is_leaf_node(item))

recursive_parsing(ast_processed)
# Test some imperative style coding
# yacc_parse.run_parser(parser, open('./php_test_files/Imperative.php', 'r'), False, False)


# Tokenize
# for tok in lexemes:
# print(lexemes.next())
# print(lexemes.lexstate)
# print(classifier.classify(tok))
# print(tok)
# print(lexemes.token())
# print(tok.value)

# Drawing the flow chart
# Drawer invocation
print()
print()
print()
print()
print()
print()

from itertools import tee, islice, chain


# For accessing previous/next elements in for loops
def previous_and_next(some_iterable):
  prevs, items, nexts = tee(some_iterable, 3)
  prevs = chain([None], prevs)
  nexts = chain(islice(nexts, 1, None), [None])
  return zip(prevs, items, nexts)


chart = None
x = fl_drawer.Drawer(chart)
for previous, drawing_entity, nxt in previous_and_next(drawable_stack):
  if drawing_entity[0] is False:
    continue

  if isinstance(drawing_entity, tuple):
    print(drawing_entity)
    if drawing_entity[1][0] == 'If':
      item_name = 'If'
      getattr(x, drawing_entity[0])(item_name)
      # print(drawing_entity[1][1]['expr'])
    else:
      item_name = 'echo ("' + drawing_entity[1][1]['nodes'][0] + '")'
      getattr(x, drawing_entity[0])(item_name)

  # Connection logic
  if previous is not None:
    x.connect('If', item_name, 'True')
  else:
    x.connect('Start', item_name)
  if nxt is None:
    x.end(item_name)
      # print(drawing_entity[1][1]['nodes'])
  # drawing_entity[1][1]['nodes'] = 'an if condition'
# x.add_process('x')
# x.connect('Start', 'x')
# x.add_decision('x == 1')
# x.connect('x', 'x == 1')
# x.add_io('y is the loveliest number')
# x.connect('x == 1', 'x is the loveliest number', 'True')
# x.connect('x == 1', 'y is the loveliest number', 'False')
# x.connect('y is the loveliest number', 'x')
# x.end('x')
# x.end('x is the loveliest number')
x.get_drawing().draw('../outputs/x.png', prog='circo')
