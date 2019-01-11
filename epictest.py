import epicbox

epicbox.configure(
    profiles=[
        epicbox.Profile('python', 'czentye/matplotlib-minimal')
    ]
)
files = [{'name': 'main.py', 'content': b'x = input(); print(x); y = input(); print("Hi " + y)'}]
limits = {'cputime': 10, 'memory': 64}
result = epicbox.run('python', 'python3 -u main.py', stdin=b'x\nalex\n', files=files, limits=limits)
print(result)

