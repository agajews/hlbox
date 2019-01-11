import hlbox
from textwrap import dedent

hlbox.configure(
    profiles=[
        hlbox.Profile('python', 'czentye/matplotlib-minimal')
    ]
)
files = [{
    'name': 'main.py', 'content': dedent(
    '''
    import json as __json
    import io as __io
    from textwrap import indent as __indent
    from contextlib import redirect_stdout as __redirect_stdout


    if __name__ == '__main__':
        __code = input()
        __string = None
        try:
            __string = __io.StringIO()
            with __redirect_stdout(__string):
                exec(eval(__code))
            __res = {'output': __string.getvalue(), 'error': None}
        except Exception as e:
            __res = {'output': __string.getvalue(), 'error': type(e).__name__ + ': ' + str(e)}
        print(__json.dumps(__res))
    ''').encode('utf-8')}]
limits = {'cputime': 1, 'memory': 64}
inpt = (repr("print('\\n'.join(['\\\\newcommand{\\cal%s}{\\mathcal{%s}}' % (c, c) for c in ['F', 'G', 'H', 'I', 'D', 'B']]))") + '\n').encode('utf-8')
box = hlbox.create('python', 'python3 -u main.py', files=files, limits=limits)

# result = hlbox.run('python', 'python3 -u main.py', stdin=inpt, files=files, limits=limits)
# print(result)

result = hlbox.runline(box, inpt)
print(result)
hlbox.destroy(box)
