import os


current_dir = os.path.dirname(os.path.realpath(__file__))

lines = []
for filename in os.listdir(current_dir):
    if os.path.isdir(filename):
        continue
    elif filename.endswith('.py'):
        with open(filename, 'r') as f:
            # for text in f:
            #     if text != '\n':
            #         lines.append(text.strip())
            lines = [line.strip() for line in f.readlines() if line != '\n']

print(lines)

with open(current_dir + '/obj.info', 'w') as f:
    for line in lines:
        f.write(line + '\n')

print('\nreading result file...')
with open(current_dir + '/obj.info', 'r') as f:
    print(f.read())
