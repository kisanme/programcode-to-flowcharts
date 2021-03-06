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

state = False


# From the classes defined with the token names,
# this method will retrieve the type of token
#
# Will return false for uncaught or whitespaces
def get_token_class(token):
  # if token.type == 'WHITESPACE':
  #   return
  for class_type in classes:
    # print(class_types)
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
    return 'add_' + class_type
  return class_type


def classify(token):
  token_class = get_token_class(token)
  if isinstance(token_class, str):
    # So the token has a class - something which is being classified by the classifier
    return method_name(get_drawer_type(token_class)), token.value
  else:
    # Something which isn't classified
    # This is intriguing because it can contain various items ranging from,
    # whitespaces
    # variable declarations
    # ** Arguments for the classified items like function call, for loop, if conditions.
    return token
