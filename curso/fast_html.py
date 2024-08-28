from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get(): return Div(P('Hello World!'), hx_get='/change', hx_swap='outerHTML')

@rt('/change')
def get(): return Div(P('Nice to be here!'), hx_get='/', hx_swap='outerHTML')

serve()