import sys

if len(sys.argv) ==  1:
  print("Command ERROR:", 'Please specify the source php file name/path')
  sys.exit(112)
if len(sys.argv) < 4:
  print("Command ERROR:", 'Please specify the output filename of the flowchart')
  sys.exit(113)

python_file_name = sys.argv[0]
php_file = sys.argv[1]
output_flowchart = sys.argv[3]

print('php file', php_file)
print('flowchart file', output_flowchart)