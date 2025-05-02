import os
import re

def splitpath(path, maxdepth=20):
     ( head, tail ) = os.path.split(path)
     return splitpath(head, maxdepth - 1) + [ tail ] \
         if maxdepth and head and head != path \
         else [ head or tail ]

def munge_title(title, max_title_length):
    match = re.match(r'\w+@([\w-]+): (.*)', title)
    if match:
        host, path = match.group(1, 2)
        dirs = splitpath(path)
        tail = dirs.pop()
        title = f'{host}: {tail}'
        if len(title) > max_title_length:
            return tail
        while dirs:
            tail = os.path.join(dirs.pop(), tail)
            newtitle = f'{host}: {tail}'
            if len(newtitle) > max_title_length:
                break
            title = newtitle
        return title
    else:
        return title
