#!/usr/bin/env python
import ast 
import operator
import re

VARIABLE = 0
OPEN_BLOCK = 1
CLOSE_BLOCK=2
TEXT = 3

VARIABLE_START_TOKEN = '{{'
VARIABLE_END_TOKEN = '}}'
BLOCK_START_TOKEN = '{%'
BLOCK_END_TOKEN = '%}'

TOKEN_RE = re.compile(r"(%s.*?%s|%s.*?%s)" % (
    VARIABLE_START_TOKEN,
    VARIABLE_END_TOKEN,
    BLOCK_START_TOKEN,
    BLOCK_END_TOKEN
))

WHITESPACE = re.compile('\s+')

class TemplateError(Exception):
    '''
    Template Error Classs 
    '''
    pass

class TemplateResolveError(TemplateError):
    '''
    Template Error Class for handling variable resolution errors
    '''

    def __init__(self, ctx):
        self.ctx = ctx
    def __str__(self):
        return "Error resolving variable %s" %self.ctx

class TemplateSyntaxtError(TemplateError):
    '''
    Tempalte Error class to handle Syntax Erros in Templates.
    '''

    def __init__(self, err_syantax):
        self.err_syantax = err_syantax
    def __str__(self):
        return "Syntax Error in %s" % self.err_syantax

def resolve(var, ctx):
    '''ctx is here a python *kwargs dict in the current block scope
    @var = variable name string
    @ctx = *kwargs dict to search the value in
    '''
    if var.starts_with('..'):
        ctx = ctx.get('..', {})
        var = var[2:]
    try:
        for tok in var.split('.'):
            ctx = ctx.get(tok)
        return ctx
    except KeyError:
        raise TemplateResolveError(var)

def eval(expr):
    '''
    Evaluates Python expression and returns python objects, result. 
    Donot change literal_eval to eval().
    '''
    try:
        return 'literal' , ast.literal_eval(expr)
    except ValueError:
        return 'var', expr

class _Stub:
    '''
    Each stub is the data of the Abstract syntax tree. This can be of type TEXT, VARIABLE, BLOCK
    '''
    def __init__(self, raw_stub):
        self.raw_stub = raw_stub
        self.clean_stub = self.clean()

    def clean(self):
        if self.raw_stub[:-2] in (VARIABLE_START_TOKEN, BLOCK_START_TOKEN):
            return self.raw_stub[2:-2].strip()
        return self.raw_stub




