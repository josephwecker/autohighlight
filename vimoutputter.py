from outputter import Outputter
from utils import Set

class VimOutputter(Outputter):
    # TODO document the builtin color names
    ColorMapping = { 'Comment': 'Comment', \
                     'Constant': 'Constant', \
                     'String': 'String', \
                     'VariableName': 'Identifier', \
                     'FunctionName': 'Function', \
                     'Keyword': 'Statement', \
                     'Type': 'Type', \
                     'None': 'NONE', \
                     'Error': 'Error' }

    def __init__(self,errorChecking=False):
        self.buffer=''
        self.colorsSeen = Set()
        self.errorChecking = errorChecking

    def appendColorDefinition(self, color):
        cterm_attrs=[]
        attrs=[]
        if('font-weight' in color.attrs):
            if(color.attrs['font-weight'] == 'bold'):
                cterm_attrs += ['bold']

        if('font-style' in color.attrs):
            if(color.attrs['font-style'] == 'italic'):
                cterm_attrs += ['italic']

        if('text-decoration' in color.attrs):
            if(color.attrs['text-decoration'] == 'underline'):
                cterm_attrs += ['underline']
            if(color.attrs['text-decoration'] == 'inverse'):
                cterm_attrs += ['inverse']

        if len(cterm_attrs) > 0:
            attrs += [ 'cterm=' + ','.join(cterm_attrs) ]

        if('color' in color.attrs):
            attrs += [ 'ctermfg='+color.attrs['color'] ]

        if('background-color' in color.attrs):
            attrs += [ 'ctermbg='+color.attrs['background-color'] ]

        self.buffer+=':hi clear %s\n' % (color.name.text)
        self.buffer+=':hi %s %s\n' % (color.name.text, ' '.join(attrs))

    def appendLiteral(self, color, literal):
        if(color.predefined):
            colorName = self.ColorMapping[color.name.text]
        else:
            colorName = color.name.text
        self.colorsSeen.add(colorName)
        self.buffer+='syn keyword %s %s\n' % (colorName,literal)

    def appendMapping(self, color, contexts):
        if(color.predefined):
            colorName = self.ColorMapping[color.name.text]
        else:
            colorName = color.name.text
        self.colorsSeen.add(colorName)
        for context in contexts:
            left_regex = '|'.join(context.getLeftRegexes())
            middle_regex = '|'.join(context.getMiddleRegexes())
            right_regex = '|'.join(context.getRightRegexes())
            self.buffer+='"Rule for %s\n'%middle_regex
            contained=''
            if(self.errorChecking):
                contained='contained'
            self.buffer+='syn match %s "\\v((%s)(\\s*\\n\\s*|\\s*))@<=(%s)\\ze(\\s*\\n\\s*|\s*)(%s)" %s\n' % (colorName,left_regex,middle_regex,right_regex,contained)
    
    def getBuffer(self):
        if(self.errorChecking):
            self.buffer += "syn region Error start='^' end='$' contains=%s,NONE\n" % ','.join(self.colorsSeen)
            self.buffer += "syn match NONE '\s' contained\n"
        return self.buffer
