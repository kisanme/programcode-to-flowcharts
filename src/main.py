import lib.phplex as phplex
import classifier.classifier as classifier
import drawer.drawer as fl_drawer

def parse_through_lex(filepath):
  data = open(filepath, 'r').read()
  phplex.full_lexer.input(data)
  return phplex.full_lexer


lexemes = parse_through_lex('./php_test_files/BasicClass.php')
# Tokenize
for tok in lexemes:
  # print(classifier.get_token_class(tok))
  # print(tok)
  print(lexemes.token())
  # print(tok.value)

chart = None
x = fl_drawer.Drawer(chart)
x.add_process('x')
x.add_io('y is the loveliest number')
x.connect('x', 'y is the loveliest number')
x.get_drawing().draw('./abc.png', prog='circo')
print()
