#!/Users/matthew/anaconda3/envs/graphics/python
import subprocess

from PyPDF2 import PdfFileReader
import numpy as np
from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions, LongTabu, HFill, TikZPathList, TikZPath,
                     NoEscape)

from pylatex.utils import bold
from copy import deepcopy


global_scale = 1
format_text = r'\fontsize{{{0}cm}}{{1pt}}\selectfont'.format(.4*global_scale)
print(format_text)

edge_thickness = 2
# edge_thickness = 4
labels=False

doc = Document(page_numbers=False, documentclass='standalone', document_options={'border': '0cm'})
# doc = Document(page_numbers=False, documentclass='article')

# doc.preamble.append(r'\usepackage{color}')
doc.preamble.append(NoEscape('\definecolor{mycolor}{RGB}{132,165,162}'))
# doc.preamble.append(NoEscape('\definecolor{edgecolor}{RGB}{0,0,0}'))
doc.preamble.append(NoEscape('\definecolor{edgecolor}{RGB}{240,0,0}'))
doc.preamble.append(NoEscape('\pgfdeclarelayer{bg}'))
doc.preamble.append(NoEscape('\pgfsetlayers{bg,main}'))

anchor = 'north west'
pic_opts = TikZOptions('shorten >= 0pt', 'shorten <= {}cm'.format(-.1 * global_scale),
                       **{'draw': 'black',
                         # 'line width': .05,
                         'inner sep': '0pt',
                         'node distance': '{}cm'.format(1 * global_scale),
                         'anchor': anchor, 'x': '{}cm'.format(global_scale), 'y': '{}cm'.format(global_scale)})

with doc.create(TikZ(options=pic_opts)) as pic:
    # def c(x, y):
        # return TikZCoordinate(x*global_scale, y*global_scale)
    c = TikZCoordinate

    nodes = []
    node_opts = TikZOptions('circle',
                            **{'line width': 3*global_scale, 'draw opacity': 0,
                            'fill opacity': 0, 'minimum size': '.7cm',
                               'inner sep': 3*global_scale})

    annot_opts = TikZOptions('circle',
                            **{'fill': 'none', 'minimum size': 1,
                               'inner sep': 3 * global_scale})


    def add_node(handle, text, x, y, options=node_opts):
        temp = TikZNode(text=format_text + text,
                        handle=handle,
                        options=options,
                        at=c(x, y))
        pic.append(temp)
        nodes.append(temp)

    if not labels:
        add_node('h1', '', 0, 0)
        add_node('h2', '', .8, 1.7)
        add_node('h3', '', 1.5, 3)
        add_node('h4', '', 3.2, 2.8)
        add_node('h5', '', 1.4, -.3)
        add_node('hN', '', 3.3, 0)
    else:
        add_node('h1', r'$h_{1}$', 0, 0)
        add_node('h2', r'$h_{2}$', .8, 1.7)
        add_node('h3', r'$h_{3}$', 1.5, 3)
        add_node('h4', r'$h_{4}$', 3.2, 2.8)
        add_node('h5', r'$h_{5}$', 1.4, -.3)
        add_node('hN', r'$h_{N}$', 3.3, 0)
    # add_node('dots', r'$\cdots$', (3.3+1.4)/2, -.3/2, options=annot_opts)
    # add_node('dots', r'$\cdots$', (3.3+1.4)/2, -.3, options=annot_opts)
    # add_node('dots', r'$\ldots$', (3.3+1.4)/2, -.3/2)


    pic.append(NoEscape(r'\begin{pgfonlayer}{bg}'))
    with pic.create(TikZDraw()) as path:
        path_base = {'line width': edge_thickness*global_scale, '>': 'stealth', 'draw': 'edgecolor'}
        # path_options = TikZOptions('->', **{'line width': 2*global_scale, '>': 'stealth'})

        bend = 30
        def add_edge(node_0, node_1, bend=bend, bend_type='left'):
            path_opts_1 = deepcopy(path_base)
            if bend_type == 'left':
                path_opts_1.update({'bend left': bend})
            else:
                path_opts_1.update({'bend right': bend})


            # path_opts_1.update({'bend left': 30, 'bend right': bend_right})

            # path_opts_1.append_positional)
            # path_options_1 = path_options
            path.append(node_0)
            path.append(TikZUserPath('edge', TikZOptions('->', **path_opts_1)))
            path.append(node_1)

        add_edge(nodes[0], nodes[1], bend_type='right')
        add_edge(nodes[1], nodes[0], bend_type='right')
        # add_edge(nodes[1], nodes[0])
        # add_edge(nodes[1], nodes[2], bend=20)
        add_edge(nodes[2], nodes[1], bend=0)
        add_edge(nodes[1], nodes[3], bend=bend, bend_type='right')
        add_edge(nodes[2], nodes[4])
        add_edge(nodes[0], nodes[4], bend=0)
        add_edge(nodes[3], nodes[5])
        add_edge(nodes[3], nodes[2], bend_type='right')
        add_edge(nodes[3], nodes[5])
        add_edge(nodes[0], nodes[5])
        # add_edge(nodes[2], nodes[3])

    pic.append(NoEscape(r'\end{pgfonlayer}'))

# doc.generate_pdf('nn_py', clean_tex=True)
# subprocess.run(["pdf2svg", 'nn_py.pdf', 'nn_py.svg'])
doc.generate_pdf('nn_py_no_nodes', clean_tex=True)
# subprocess.run(["pdf2svg", 'nn_py_thick.pdf', 'nn_py_thick.svg'])
