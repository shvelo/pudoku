#!/usr/bin/env python
#
#Pudoku, A web interface sudoku
#Copyright (c) 2012, Sina Samavati
#Licensed under the BSD License http://www.opensource.org/licenses/BSD-3-Clause


from flask import Flask, render_template, request, url_for
from optparse import OptionParser
from lib import sudoku

app = Flask(__name__)

# Generate a sudoku
def pudo(difficulty=0):
    pu = sudoku.Sudoku(difficulty=difficulty)
    do = [str(e) for e in pu.masked_grid]
    ku = ['<div class="pudoku"><form action="result" method="POST">\n']
    l = [i*27 for i in xrange(4)]
    c = 0

    for n in do:

        if c in l:
            ku.append('%s\n<br> +%s+ <br>\n' % ('|' if c != 0 else '', '-' * 80))

        if c % 9 == 0 and c not in l:
            ku.append('|\n<br>\n')

        if c % 3 == 0:
            ku.append('|')

        ku.append('<input align="top" type="text" %s value="%s" name="%s" maxlength="1">\n' \
                      % ('readonly="readonly"' if n else '', n, str(c)))

        c += 1

    ku.append('|\n<br> +%s+ <br />' % ('-' * 80))
    ku.append('\n<br><br>\n<input class="btn primary" type="submit" value="Submit" name="submit"></form></div>')
    pudoku = ' '.join(ku)
    global solution
    solution = pu.solution
    for i in xrange(len(solution)):
        solution[i] = unicode(solution[i])

    return pudoku

# Generate the template
def template(title='Pudoku', body=None):
    content = render_template('layout.html')
    return content % {'title': title,
                      'content': body}

# Detect pathes and send response to the http server
@app.route('/')
def index():
    return template(body=render_template('index.html'))

# Generate the game with a level
@app.route('/easy')
def easy():
    return template(title='Easy - Pudoku', body=pudo())

@app.route('/medium')
def medium():
    return template(title='Pudoku - Medium', body=pudo(1))

@app.route('/hard')
def hard():
    return template(title='Pudoku - Hard', body=pudo(2))

@app.route('/result', methods=['POST'])
def result():
    form = [request.form[str(i)] for i in xrange(len(solution))]
    if form == solution:
        return template(title='Win',
                        body='<h2>Congratulations!</h2><center><p>You won the game!</p></center>')

    else:
        return template(title='Lose',
                        body='<h2>Sorry!</h2><center><p>You haven\'t been able to win the game</p></center>')


def main():
    parser = OptionParser(description='Pudoku is a web interface sudoku', 
                          version='Pudoku 1.1.3')
    parser.add_option('--host', type='str', default='localhost', 
                      help='\tHost to bind')
    parser.add_option('--port', type='int', default=5000,
                      help='\tPort to bind')

    help_context = {'--version': '\tDisplay current version',
                    '--help': '\tDisplay this help message and exit'}

    # A simple hack
    for counter in xrange(len(parser.option_list)):
        option = parser.option_list[counter].get_opt_string()
        if option in help_context:
            parser.option_list[counter].help = help_context[option]

    opt  = parser.parse_args()[0]
    host = opt.host
    port = opt.port
    app.run(host=host, port=port)
    

if __name__ == '__main__':
    main()

# I hope it's useful
