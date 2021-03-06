import src.drawer.drawer as fl_drawer
'''
# While loop drawing
while_drawer = fl_drawer.Drawer(None)
while_drawer.connect('Start', '$counter = 0;')
while_drawer.add_process('$counter = 0;')
while_drawer.connect('$counter = 0;', '$counter < 100')
while_drawer.add_decision('$counter < 100')
while_drawer.connect('$counter < 100', '$some_array[] = $counter;', 'True')
while_drawer.add_process('$some_array[] = $counter;')
while_drawer.connect('$some_array[] = $counter;', '$counter ++;')
while_drawer.add_process('$counter ++;')
while_drawer.connect('$counter ++;', '$counter < 100')
while_drawer.end('$counter < 100', 'False')
while_drawer.get_drawing().draw('../outputs/while.png', prog='dot')
'''

# Nested If condition
if_drawer = fl_drawer.Drawer(None)
if_drawer.connect('Start', 'par_if')
if_drawer.add_decision('if ($x == 0)', 'par_if')
if_drawer.add_decision('if ($y == 0)', 'child_if')
if_drawer.connect('par_if', 'child_if', 'True')
if_drawer.connect('child_if', 'tt', 'True')
if_drawer.connect('child_if', 't', 'False')
if_drawer.connect('par_if', 'f', 'False')
if_drawer.connect('tt', 't')
if_drawer.add_process('$y = 20', 'tt')
if_drawer.add_process('$y = $y + 20', 't')
if_drawer.add_process('$y = 10', 'f')
if_drawer.end('t')
if_drawer.end('f')
if_drawer.get_drawing().write('../outputs/nested_if_else_mod.dot')
if_drawer.get_drawing().draw('../outputs/nested_if_else_mod.png', prog='dot')

'''
# Single If condition
si_draw = fl_drawer.Drawer(None)
si_draw.connect('Start', 'if ($x == 0)')
si_draw.add_decision('if ($x == 0)')
si_draw.connect('if ($x == 0)', '$y = 20', 'True')
si_draw.connect('if ($x == 0)', '$y = 10', 'False')
si_draw.end('$y = 10')
si_draw.connect('$y = 20', 'End')
si_draw.get_drawing().write('../outputs/single_if_else.dot')
si_draw.get_drawing().draw('../outputs/single_if_else.png', prog='dot')
'''

# Mixed Constructs
mi_draw = fl_drawer.Drawer(None)
mi_draw.connect('Start', 'init')
mi_draw.add_process('$c = 1', 'init')
mi_draw.add_decision('$c <= 10', 'while_cond')
mi_draw.add_process('$c += 1', 'inc')
mi_draw.add_decision('$c % 2 == 0', 'even_num_cond')
mi_draw.add_io('echo("$c is an even number")', 'tt')
mi_draw.add_io('echo("$c is an odd number")', 'tf')
mi_draw.connect('init', 'while_cond')
mi_draw.connect('while_cond', 'even_num_cond', 'True')
mi_draw.connect('even_num_cond', 'tt', 'True')
mi_draw.connect('even_num_cond', 'tf', 'False')
mi_draw.connect('tt', 'inc')
mi_draw.connect('tf', 'inc')
mi_draw.connect('inc', 'while_cond')
mi_draw.end('while_cond', 'False')
mi_draw.get_drawing().write('../outputs/mixed_constructs.dot')
mi_draw.get_drawing().draw('../outputs/mixed_constructs.png', prog='dot')
