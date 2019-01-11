import hlbox

hlbox.configure(
    profiles=[
        hlbox.Profile('python', 'czentye/matplotlib-minimal')
    ]
)
files = [{'name': 'main.py', 'content': b'x = input(); print(x); y = input(); print("Hi " + y)'}]
limits = {'cputime': 10, 'memory': 64}
box = hlbox.create('python', 'python3 -u main.py', files=files, limits=limits)
# result = hlbox.run('python', 'python3 -u main.py', stdin=b'x\nalex\n', files=files, limits=limits)
# print(result)

result = hlbox.runline(box, b'x\n')
print(result)
result = hlbox.runline(box, b'alex\n')
print(result)

hlbox.destroy(box)
