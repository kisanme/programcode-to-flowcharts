from unittest.mock import _get_method

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
  ]
}


# From the classes defined with the token names,
# this method will retrieve the type of token
#
# Will return false for uncaught or whitespaces
def get_token_class(token):
  if token.type == 'WHITESPACE':
    return False
  for class_type in classes:
    if token.type in classes[class_type]:
      return class_type
  return False
