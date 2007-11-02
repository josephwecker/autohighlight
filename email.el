(defgroup email-group nil "Customizations for email-mode.")
(defconst email-font-lock-keywords
  '(("\\(?:\:\\)\\s-*\\([A-Za-z][-A-Za-z0-9_]*\\)\\s-*\\(?:\;\\)"
     ;;Highlight typeUse
     (1 'font-lock-type-face))
    ("\\(?:\\<var\\>\\)\\s-*\\([A-Za-z][-A-Za-z0-9_]*\\)\\s-*\\(?:\:\\)"
     ;;Highlight idDef
     (1 'font-lock-string-face))
    ("\\(?:\\`\\|\;\\)\\s-*\\([A-Za-z][-A-Za-z0-9_]*\\)\\s-*\\(?:\=\\)"
     ;;Highlight idUse
     (1 'font-lock-variable-name-face))
    ("\\(?:\=\\)\\s-*\\([A-Za-z][-A-Za-z0-9_]*\\)\\s-*\\(?:\;\\)"
     ;;Highlight idUse
     (1 'font-lock-variable-name-face))
    ("\\(?:\\<Print\\>\\)\\s-*\\([A-Za-z][-A-Za-z0-9_]*\\)\\s-*\\(?:\;\\)"
     ;;Highlight idUse
     (1 'font-lock-variable-name-face))
    ("\\(?:\\`\\|\;\\)\\s-*\\(\\<var\\>\\)\\s-*\\(?:[A-Za-z][-A-Za-z0-9_]*\\)"
     ;;Highlight 'var'
     (1 'font-lock-keyword-face))
    ("\\(?:\\`\\|\;\\)\\s-*\\(\\<Print\\>\\)\\s-*\\(?:[0-9]+\\|[A-Za-z][-A-Za-z0-9_]*\\)"
     ;;Highlight 'Print'
     (1 'font-lock-keyword-face))
    ("\\(?:\=\\)\\s-*\\([0-9]+\\)\\s-*\\(?:\;\\)"
     ;;Highlight int
     (1 'font-lock-constant-face))
    ("\\(?:\\<Print\\>\\)\\s-*\\([0-9]+\\)\\s-*\\(?:\;\\)"
     ;;Highlight int
     (1 'font-lock-constant-face))))
(defun email-mode ()
  (interactive)
  (kill-all-local-variables)
  (setq major-mode 'email-mode
        mode-name "email"
        fill-column 74
        indent-tabs-mode t
        tab-width 4)
  (set (make-local-variable 'require-final-newline) t)
  (set (make-local-variable 'next-line-add-newlines) nil)
  (set (make-local-variable 'font-lock-defaults)
       '(email-font-lock-keywords nil nil nil backward-paragraph (font-lock-lines-before . 2) (font-lock-lines-after . 2)))
  (set (make-local-variable 'font-lock-lines-before) 2))
