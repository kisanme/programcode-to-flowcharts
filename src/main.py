import lib.phplex as phplex
import lib.phpparse as yacc_parse
import translator.toflow as toflow
import pprint
import classifier.classifier as classifier
import drawer.drawer as fl_drawer


# Parsing invocation
def parse_through_lex(file_path):
  data = open(file_path, 'r').read()
  phplex.full_lexer.input(data)
  return phplex.full_lexer


def recursive_parsing(nodes):
  if nodes is False:
    return

  print('inside the recursive parser')
  if toflow.is_leaf_node(nodes):
    print('leaf node', nodes)
    return nodes
  else:
    for node in nodes:
      if not toflow.is_leaf_node(node):
        print('none leaf node:', node)
        if isinstance(node, tuple):
          print('tuple item')
          recursive_parsing(toflow.get_nodes(toflow.get_node_attributes(node)))
        else:
          print('list or dict or other item')
          recursive_parsing(toflow.get_nodes(node))
        # return x
      else:
        print('leaf2 node:', node)

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


(recursive_parsing(ast_processed))
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
chart = None
x = fl_drawer.Drawer(chart)
x.add_process('x')
x.connect('Start', 'x')
x.add_decision('x == 1')
x.connect('x', 'x == 1')
x.add_io('y is the loveliest number')
x.connect('x == 1', 'x is the loveliest number', 'True')
x.connect('x == 1', 'y is the loveliest number', 'False')
x.connect('y is the loveliest number', 'x')
x.end('x')
x.end('x is the loveliest number')
x.get_drawing().draw('../outputs/abc.png', prog='circo')
