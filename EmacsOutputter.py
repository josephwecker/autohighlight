from outputter import Outputter
import re
class EmacsOutputter(Outputter):
    # TODO this needs to go in the docs
    """You absolutely MUST have an EMACS newer than September 2005. It
    was in Sept of 2005 that multi-line highlighting capacity first
    came to Emacs.
    
    You can get it this way:
    cvs -d:pserver:anonymous@cvs.savannah.gnu.org:/sources/emacs co emacs
    cd emacs && ./configure && make && sudo make install"""
    ## TODO: Encapsulate this in CUSTOMIZE... so the user can redefine colors, indents, etc, without having to modify the file
    def __init__(self, name="autohighlight"):
        self.name, self.colordefs, self.mapping, self.literals = name, [], [], []
        self.predef = { 'Comment': 'font-lock-comment-face', \
                        'Constant': 'font-lock-constant-face', \
                        'String': 'font-lock-string-face', \
                        'VariableName': 'font-lock-variable-name-face', \
                        'FunctionName': 'font-lock-function-name-face', \
                        'Keyword': 'font-lock-keyword-face', \
                        'Type': 'font-lock-type-face', \
                        'None': 'font-lock-default-face', \
                        'Error': 'font-lock-warning-face' }
    # XXX need to plug something in for font-lock-default-face

    def appendColorDefinition(self, color):
        self.guaranteeEmacsName(color)
        self.colordefs += [color]
        pass

    def appendLiteral(self, color, literal):
        self.guaranteeEmacsName(color)
        self.literals +=[ [ color, literal ]]
        pass

    def appendMapping(self, color, contexts):
        self.guaranteeEmacsName(color)
        self.mapping += [[color, contexts]]

    def guaranteeEmacsName(self, color):
        if color.predefined:
            color.emacs_name = self.predef[color.name.text]
        else:
            color.emacs_name = "font-lock-%s-%s-face" % (self.name, color.name.text)

    def getColorDefinitions(self):
        """Produce defface forms"""
        # cssMappers is a hash whose values are functions taking the
        # value the user provided and returning a lisp form (sans
        # parentheses)
        cssMappers = { 'font-family': lambda x: 'face %s' % x, \
                       'font-style': lambda x: 'slant %s' % x, \
                       'font-weight': lambda x: 'weight %s' % x, \
                       'font-size': lambda x: 'height %s' % int(x) * 10,
                       'text-decoration': \
                           lambda x: "%s t" % { 'underline': 'underline', \
                                                'overline': 'overline',\
                                                'line-through': 'strike-through',\
                                                'inverse' : 'inverse-video' }[x], \
                       'color': lambda x: 'foreground "%s"' % x,
                       'background-color': lambda x: 'background "%s"' % x
                     }
        rt = ""
        for color in self.colordefs:
            rt += "(defface %s\n" % color.emacs_name
            rt += "  '((t "
            rt += "\n       ".join([ "(:%s)" % cssMappers[attr](val) \
                for attr,val in color.attrs.iteritems() ])
            rt += "))\n"
            rt += "  \"Generated face for highlighting %ss\"\n" % color.name.text
            rt += "  :group '%s-faces)\n\n" % self.name
        return rt

    def getFontLockKeywords(self):
        """This function builds the font-lock-keywords constant from
        the colorings the user requested."""
        def filter_regexp(s):
            """Emacs regular expressions are different from normal
            regular expressions, so at this stage, we attempt to
            sanely convert ordinary regexes into emacs regexes. It
            probably is missing edge cases.

            IMPORTANT NOTE ABOUT COLORING CORRECTNESS: Emacs CAN and
            WILL highlight multiple lines at once, but the instant you
            edit a line, emacs considers only the current line when
            recoloring it. That means if you rely on a semicolon in
            the previous line in order to color the first element of
            this line, you'll run into problems. The horrible hacky
            solution is to replace the %^ beginning of document with
            the emacs-y beginning of line or beginning of document.
            This is only the case for emacs made before the date
            listed at the top of this file. If you have an emacs newer
            than this (which you'll need anyway because even though
            older versions can highlight, they don't deal with
            change), leave this function alone."""
            left = ""
            right = ""
            if s[0].isalnum():
                left = "\\\\<"
            if s[-1].isalnum():
                right = "\\\\>"
            s = re.sub(re.escape("%^"), "\\\\\\\\`", s)
            s = re.sub(re.escape("%$"), "\\\\\\\\'", s)
            return left + re.sub("(?<!\\\\)\\|", "\\\\\\\\|", s) + right
        # TODO: Emacs pragma to set the documentation for this keyword
        rt = "(defconst %s-font-lock-keywords\n" % self.name
        rt += "  '("
        map_lines = []
        for (color, contexts) in self.mapping:
            for context in contexts:
                pre = "\\\\|".join(context.getLeftRegexes())
                sym = "\\\\|".join(context.getMiddleRegexes())
                post = "\\\\|".join(context.getRightRegexes())
                fmt = '\\\\s-*'.join(['\\\\(%s\\\\)']*3)
                fmt = '("' + fmt + ("\"\n     ;;Highlight %s\n     (1 '%s))" \
                                    % (context.middleSymbol.defining_token.text, color.emacs_name))
                s = fmt % ("?:" + filter_regexp(pre), filter_regexp(sym), "?:"+filter_regexp(post))
                map_lines += [s]
        for (color, literal) in self.literals:
            #map_lines += ["(\"\\\\<\\\\(%s\\\\)\\\\>\"\n     (0 '%s))" % (literal, colorname)]
            map_lines += ["(\"\\\\(%s\\\\)\"\n     (0 '%s))" % (literal, color.emacs_name)]
        rt += "\n    ".join(map_lines)
        rt += "))\n"
        return rt

    def getModeFunction(self):
        rt = "(defun %s-mode ()\n" % self.name
        rt += "  (interactive)\n"
        rt += "  (kill-all-local-variables)\n"
        rt += "  (setq major-mode '%s-mode\n" % self.name
        rt += "        mode-name \"%s\"\n" % self.name
        rt += "        fill-column 74\n"
        rt += "        indent-tabs-mode t\n"
        rt += "        tab-width 4)\n"
        rt += "  (set (make-local-variable 'require-final-newline) t)\n"
        rt += "  (set (make-local-variable 'next-line-add-newlines) nil)\n"
        rt += "  (set (make-local-variable 'font-lock-defaults)\n"
        #               keywords              kwds-only  case-fold  syntax-alist  syntax-begin  other-variables
        rt += "       '(%s-font-lock-keywords nil nil nil backward-paragraph (font-lock-lines-before . 2) (font-lock-lines-after . 2)))\n" % self.name
        rt += "  (set (make-local-variable 'font-lock-lines-before) 2))\n"
        #rt += "(font-lock-lines-before . 2)"
        #rt += ")))\n"
        return rt

    def getGroupDefinition(self):
        rt = "(defgroup %s-group nil \"Customizations for %s-mode.\")\n" % \
             (self.name, self.name)
        return rt

    def getBuffer(self):
        rt = self.getGroupDefinition()
        rt += self.getColorDefinitions()
        rt += self.getFontLockKeywords()
        rt += self.getModeFunction()
        return rt

if __name__ == "__main__":
    from ah import generate_emacs
    generate_emacs("mystery.ah")

