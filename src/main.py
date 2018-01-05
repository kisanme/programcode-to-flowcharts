import lib.phplex as phplex

def parse_through_lex(filepath):
  data = open(filepath, 'r').read()
  phplex.full_lexer.input(data)
  return phplex.full_lexer


lexemes = parse_through_lex('./php_test_files/BasicClass.php')
# Tokenize
for tok in lexemes:
  print(tok.type)
  print(tok.value)
