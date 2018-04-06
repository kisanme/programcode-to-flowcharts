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

          if (processed_node is not None) and isinstance(processed_node, tuple):
            ''' 
              This is buggy: It only checks the very first node item, say the first statement of the block
            '''
            drawable = tf.identify_translate_to(processed_node[0]), processed_node
            # print('DRAWABLE')
            # pprint.pprint(drawable[0])

            # print('DRAWABLE-0:', drawable[0])
            # if isinstance(drawable[0], str) and (drawable[0] != False) and (drawable[0] in ['add_io', 'add_process', 'add_decision']):
            #   drawable_stack.append(drawable)
            # print('drawable (from list):', drawable_stack)
          # #print('processed_node list:', processed_node)
          # drawable_stack.append((tf.get_node_type(node), recursive_shallow_parsing(tf.get_nodes(node))))
          elif (processed_node is not None) and isinstance(processed_node, list) and len(processed_node) == 1:
            ''' 
              When there is only a single node within the method block
            '''
            processed_node = recursive_shallow_parsing(processed_node[0])
            drawable = tf.identify_translate_to(processed_node), processed_node
            if isinstance(drawable[0], str) and (drawable[0] != False) and (drawable[0] in ['add_io', 'add_process', 'add_decision']):
              drawable_stack.append(drawable)

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


'''
  IO node manipulation.
  The node will be obtained after shallow parsing.
'''
def io_node(node):
  shape = tf.identify_translate_to(node)
  output_text = tf.get_processed_text_from_node(node)
  # print('SHAPE', shape)
  # print('OUTPUT TEXT', output_text)
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
    'while_last': []
  })
  node_type = tf.get_node_type(node)
  print('NODE TYPE', node_type)
  if node_type in ['If', 'ElseIf', 'While']:
    else_items = []
    elif_container = []

    expression = tf.get_node_values(node[1], 'expr')
    true_items = tf.get_node_values(tf.get_node_values(node[1], 'node')[1], 'nodes')
    # if (true_items[0][0] == 'If'):
      # print('If within if')
      # true_items = tf.get_node_values(tf.get_node_values(true_items[0][1], 'node')[1], 'nodes')
      # pprint.pprint(true_items)
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
      '''
        Recursively calls the same method to generate the if within if block
      '''
      print("TRUE ITEMS:")
      pprint.pprint(i)
      if i[0] == 'If':
        print('IFFED')
        rd_if = decision_node(i)
        print('CONSTRUCTED')
        pprint.pprint(rd_if)
        # pprint.pprint(rd_if)
        # mapped_drawer = tf.identify_translate_to(i)
        # shape_text = tf.get_processed_text_from_node(i)
        decision_output[1]['true'].append(rd_if)
      else:
        print('true item: ')
        pprint.pprint(i)
        mapped_drawer = tf.identify_translate_to(i)
        shape_text = tf.get_processed_text_from_node(i)
        decision_output[1]['true'].append((mapped_drawer, shape_text))
        # print(mapped_drawer)
        # print(shape_text)

    '''
      Recursively calls the same method to generate the else-if block
    '''
    for el_if in elif_container:
      '''
        Recursively calls the same method to generate the if within if block
      '''

      print("ELIF ITEMS:")
      pprint.pprint(el_if)
      if el_if[0] == 'If':
        print('ELIF if')
        pprint.pprint(el_if)
        rd_if = decision_node(el_if)
        decision_output[1]['true'].append(rd_if)
      else:
        print('ELIF if else')
        pprint.pprint(el_if)
        rd_built = decision_node(el_if)
        decision_output[1]['false'].append(rd_built)

    # print()
    for i in else_items:
      '''
        Recursively calls the same method to generate the if within else block
      '''
      if i[0] == 'If':
        rd_if = decision_node(i)
        decision_output[1]['true'].append(rd_if)
      else:
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

    '''
      WHILE Node evaluation
      Add the pointer to the last_node to the WHILE condition
    '''
    if node_type == 'While':
      decision_output[1]['while_last'].append((mapped_drawer, shape_text))
      
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
  num_t_t_items = 0
  num_else_items = 0
  while_last_item_id = 0
  t_count = 0
  f_count = 0
  t_t_cond_id = None

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
    '''
      True side of the condition
    '''
    for t_item in item[1]['true']:
      if (not isinstance(t_item[0], str)):
        continue
      
      # If block within the true block of a parent if (true within true)
      num_t_t_items = 0
      if(isinstance(t_item[0], str) and t_item[0] == 'add_decision'):
        print('DECISION DRAW')
        pprint.pprint(t_item)

        t_t_cond_id = t_count + 1110
        t_t_count = t_t_cond_id

        drawing_shape = getattr(res_draw, t_item[0])
        drawing_shape(t_item[1]['condition'], t_t_cond_id)

        # print('Connection count', f_count+1, el_if_cond_id)
        # Connect 'true' edge to the 1st node within the block
        res_draw.connect(t_t_cond_id, t_t_count+1, 'True')
        num_t_t_items += 1

        '''
          True items within the second if block
        '''
        for e_if_item in t_item[1]['true']:
          t_t_count += 1
          drawing_shape = getattr(res_draw, e_if_item[0])
          drawing_shape(e_if_item[1], t_t_count)
          # print('THANI block', t_t_cond_id)

          # Connect the nodes within a single else-if block
          print(t_t_count-1, t_t_cond_id)
          if (t_t_count-1 != t_t_cond_id):
            res_draw.connect(t_t_count-1, t_t_count)
            print()

          
          # Increment the number of ELSE-IF statements
          num_t_t_items += 1
        
        # Connect the last node within sub-if to the nodes outside
        res_draw.connect(t_t_count, t_count+1)

        if(t_item[1]['false'] == []):
          res_draw.connect(t_t_cond_id, t_count+1, 'False')

      else:
        print('T', t_item)
        drawing_shape = getattr(res_draw, t_item[0])
        drawing_shape(t_item[1], t_count)

      if num_t_t_items > 0:
        print(res_draw.get_nodes())
        res_draw.connect(t_count-1, t_t_cond_id)
        print('T', t_count)

      '''
        If there is true elments
      '''
      if t_count > 1110:
        '''
          If the t_count doesn't exist, it doesn't draw the connection
        '''
        try:
          if (res_draw.get_node(t_count) and res_draw.get_node(t_count-1)):
            res_draw.connect(t_count-1, t_count)
        except KeyError:
          pass

      # Last of the while block
      # This is to identify the looping statement
      if (len(item[1]['while_last']) > 0):
        while_last_item_id = t_count
      
      # Increment the true count for the next item of the loop
      t_count += 1

    
  # Draw the connection from last item of within the while block to the conditional block
  if (len(item[1]['while_last']) > 0):
    res_draw.connect(while_last_item_id, cond_id)

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

        # print('ELIF condition id', el_if_cond_id)
        drawing_shape = getattr(res_draw, e_item[0])
        drawing_shape(e_item[1]['condition'], el_if_cond_id)

        # Drawing ELSE-IF conditionally true block
        if len(e_item[1]['true']) > 0:

          # print('Connection count', f_count+1, el_if_cond_id)
          # Connect 'true' edge to the 1st node within the block
          res_draw.connect(el_if_cond_id, f_count+1, 'True')
          num_el_if_items += 1

          for e_if_item in e_item[1]['true']:
            f_count += 1
            drawing_shape = getattr(res_draw, e_if_item[0])
            drawing_shape(e_if_item[1], f_count)
            # print('THANI block', f_count)

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
        print(last_el_if_ids)
        if f_count > el_if_cond_id and last_el_if_id and f_count > max(*last_el_if_ids)+1:
          res_draw.connect(f_count-1, f_count)
        

      '''
        Link all items within the false block, when there is a nested if condition
      '''
      if f_count > 10000 and t_t_cond_id and t_t_cond_id > 0:
        '''
          If the f_count doesn't exist, it doesn't draw the connection
        '''
        try:
          if (res_draw.get_node(f_count) and res_draw.get_node(f_count-1)):
            res_draw.connect(f_count-1, f_count)
        except KeyError:
          pass

      f_count += 1

    '''
    # The last node of else block connects to the rest of 
    #   the statement outside the else block
    '''
    # Connect every ending node of ELSE-IF block to the rest of outer sphere
    [res_draw.connect(lif_node_id, count+1) for lif_node_id in last_el_if_ids]

    # BUG
    # When there is no element outside the if-else block, this creates a new element
    # res_draw.connect(f_count-1, count+1)
    
    # Returns the latest count for each item
  return count, t_count, f_count


def draw_results(draw_list, output_path):
  count = 1
  res_draw = fld.Drawer(None, debug=True)
  res_draw.initialize_drawing()
  cond_id = count
  l_count, t_count, f_count = 0, 0, 0
  # This is buggy, but yet works with one single while loop
  is_while = False

  for item in draw_list:
    '''
      Drawing simple shapes like single line statements
      $x = 'hello world';
    '''
    print("DRAW_RESULTS method")
    pprint.pprint(item)

    '''
      Adding the conditional check to use only tuples
      with the first element as a string
    '''
    if isinstance(item, tuple) and isinstance(item[0], str):
      drawing_shape = getattr(res_draw, item[0])
      if isinstance(item[1], str):
        drawing_shape(item[1], count)
        if (count-1 != cond_id):
          res_draw.connect(count-1, count)
        if cond_id == 1:
          ''' There is no condition in the resultant drawing '''
          res_draw.connect(count-1, count)

      
      '''
        Blocked statement - Complex statements
        Like If-else-elseif and While
      '''
      if isinstance(item[1], dict):
        cond_id = count
        l_count, t_count, f_count = condition_drawing(drawing_shape, res_draw, item, cond_id)
        '''
          Makes is_while with the value True if the while_last element is not empty
        '''
        is_while = item[1]['while_last'] != []

        print('Complex BLOCK:', count, item)
        # print('LATEST COUNTS', l_count, t_count, f_count)

      '''
        When the false block of if-else needs to connect to the outer block
      '''
      if l_count+1 == count and f_count > 0:
        # print('LATEST COUNTS', l_count, t_count, f_count, count)
        res_draw.connect(f_count-1, count)

    # The last node of if-true block connects to the rest of 
    #   the statement outside the else block
    # Check if this is not a while loop and the very next element after the while loop
    #   (not is_while and count == t_count-1)
    if t_count != 0 and count == l_count+1 and not is_while:
      if (is_while):
        print()
      else:
        res_draw.connect(t_count-1, l_count+1)
    elif f_count != 0 and count == l_count+1:
      res_draw.connect(f_count-1, l_count+1)
    elif is_while:
      try:
        res_draw.connect(cond_id, l_count+1, 'False')
      except KeyError:
        pass


    count += 1
  

  '''
    END NODE
  '''
  all_nodes_in_reverse = [x for x in res_draw.get_nodes()[::-1]]
  if count-1 == int(res_draw.get_nodes()[-1]):
    '''
      If the last item is less then 1 from the current count, which is 1+ the original last node
    '''
    res_draw.end(count-1)
  else:
    '''
      Adds all those elements before the last shallow node into the END node
    '''
    for node in all_nodes_in_reverse:
      node = int(node)
      if node == count-1:
        break
      res_draw.end(node)
  res_draw.get_drawing().write(output_path + '.dot')
  res_draw.get_drawing().draw(output_path + '.png', prog='dot')

    # res_draw.add_process('$counter = 0;')



def code_to_flow(php_file_path, output_path):
  # Parsing
  # lexemes = parse_through_lex('./php_test_files/BasicClass.php')
  parser = yacc_parse.make_parser()
  parsed_ast = yacc_parse.run_parser(parser, open(php_file_path, 'r'), True, False)
  # pprint.pprint(parsed_ast)

  # Removes empty elements
  ast_processed = []
  for statement in parsed_ast:
    if hasattr(statement, 'generic'):
      statement = statement.generic()
      ast_processed = statement

  print('AST:')
  pprint.pprint(ast_processed)
  print()
  # This populates drawable_stack list
  rp_parsed = shallow_parse(ast_processed)

  print()
  print('Drawable stack: ')
  pprint.pprint(drawable_stack)

  # Deep parse the shallow parsed tree
  drawing_list = []
  for node in drawable_stack:
    n_type = node[0]
    # print('shallow_node')
    # print(node)
    drawing_list.append(deep_parse(node[1], n_type))

  # print('FINAL DRAWING:')
  # pprint.pprint(drawing_list)
  draw_results(drawing_list, output_path)
