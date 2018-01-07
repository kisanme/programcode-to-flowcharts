classes = {
  'condition_start': [
    'IF',
    'ELSEIF'
  ],
  'condition_end': [
    'ENDIF',
    # 'RBRACE'
  ],
  'condition_else': [
    'ELSE'
  ],
  'switch_start': [
    'SWITCH'
  ],
  'switch_end': [
    'ENDSWITCH'
  ],
  'case': [
    'CASE'
  ],
  'for': [
    'FOR'
  ]
}

class_types = {
  'decision': [
    'condition_start',
    'case',
    'for'
  ]
}


# From the classes defined with the token names,
# this method will retrieve the type of token
#
# Will return false for uncaught or whitespaces
def get_token_class(token):
  if token.type == 'WHITESPACE':
    return
  for class_type in classes:
    if token.type in classes[class_type]:
      return class_type
  # Yet un-identified items
  return token.type, token.value


def get_drawer_type(class_type):
  for drawer_type in class_types:
    if class_type in class_types[drawer_type]:
      return drawer_type
  return None


def method_name(class_type):
  if class_type in ['decision', 'io', 'process']:
    return 'add_'+class_type
  return class_type


def classify(token):
  token_class = get_token_class(token)
  if isinstance(token_class, str):
    return method_name(get_drawer_type(token_class))
