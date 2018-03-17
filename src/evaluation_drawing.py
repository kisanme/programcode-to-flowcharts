import src.drawer.drawer as fl_drawer

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

# Nested If condition
if_drawer = fl_drawer.Drawer(None)
if_drawer.connect('Start', 'if ($x < 2)')
if_drawer.add_decision('if ($x < 2)')
if_drawer.connect('if ($x < 2)', 'if ($x == 0)', 'True')
if_drawer.connect('if ($x < 2)', 'echo ("positive numbers greater than 2")', 'False')
if_drawer.add_io('echo ("positive numbers greater than 2")')
if_drawer.add_decision('if ($x == 0)')
if_drawer.connect('if ($x == 0)', 'echo ("Zero test")', 'True')
if_drawer.add_io('echo ("1 or negative number")')
if_drawer.connect('if ($x == 0)', 'echo ("1 or negative number")', 'False')
if_drawer.add_io('echo ("Zero test")')
if_drawer.end('echo ("Zero test")')
if_drawer.connect('echo ("Zero test")', 'End')
if_drawer.connect('echo ("1 or negative number")', 'End')
if_drawer.connect('echo ("positive numbers greater than 2")', 'End')
if_drawer.get_drawing().write('../outputs/nested_if_else.dot')
if_drawer.get_drawing().draw('../outputs/nested_if_else.png', prog='dot')

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

