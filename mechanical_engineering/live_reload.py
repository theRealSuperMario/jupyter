#!/usr/bin/env python
from livereload import Server, shell
server = Server()
server.watch('source/*.rst', shell('make html', cwd='.'))
server.serve(root='build/html')