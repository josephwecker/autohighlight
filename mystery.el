(defgroup mystery-group nil "Customizations for mystery-mode.")
(defconst mystery-font-lock-keywords
  '(("\\(?:\\<OF\\>\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\=\\|BEGIN\\|\)\:\\|\;\\|\)\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\=\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\\<BEGIN\\|\;\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\:\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\=\\|BEGIN\\|\)\:\\|\;\\|\)\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\:\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\\<BEGIN\\|\;\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\)\:\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\=\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\:\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\;\\|\)\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\:\\)\\s-*\\(\\<INTEGER\\>\\)\\s-*\\(?:\)\:\\|\;\\|\)\\)"
     ;;Highlight 'INTEGER'
     (1 'font-lock-type-face))
    ("\\(?:\\<THEN\\|BEGIN\\|\]\\|END\\|DO\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\=\\|\;\\|ELSE\\|\\`\\|INTEGER\\|\)\\)\\s-*\\(\\<BEGIN\\>\\)\\s-*\\(?:\\<DO\\|RETURN\\|THEN\\|ELSE\\|[-]?[0-9]+\\|WHILE\\|PRINT\\|VAR\\|PROCEDURE\\|IF\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\=\\|\;\\|\\`\\|TYPE\\|\(\\)"
     ;;Highlight 'BEGIN'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|THEN\\|BEGIN\\|\;\\|ELSE\\>\\)\\s-*\\(\\<PRINT\\>\\)\\s-*\\(?:[-]?[0-9]+\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\(\\)"
     ;;Highlight 'PRINT'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|THEN\\|\]\\|\;\\|ELSE\\|[-]?[0-9]+\\|END\\|\)\\)\\s-*\\(\\<END\\>\\)\\s-*\\(?:\\<BEGIN\\|\;\\)"
     ;;Highlight 'END'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|THEN\\|\]\\|\;\\|ELSE\\|[-]?[0-9]+\\|END\\|\)\\)\\s-*\\(\\<END\\>\\)\\s-*\\(?:\\<END\\|\;\\|ELSE\\>\\)"
     ;;Highlight 'END'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|THEN\\|\]\\|\;\\|ELSE\\|[-]?[0-9]+\\|END\\|\)\\)\\s-*\\(\\<END\\>\\)\\s-*\\(?:\\'\\|END\\|\;\\|ELSE\\>\\)"
     ;;Highlight 'END'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<THEN\\|BEGIN\\|\\`\\|DO\\|\=\\|\;\\|ELSE\\>\\)\\s-*\\(\\<VAR\\>\\)\\s-*\\(?:[a-zA-Z][a-zA-Z0-9.\-]*\\)"
     ;;Highlight 'VAR'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<THEN\\|BEGIN\\|\\`\\|DO\\|\=\\|\;\\|ELSE\\>\\)\\s-*\\(\\<TYPE\\>\\)\\s-*\\(?:[a-zA-Z][a-zA-Z0-9.\-]*\\)"
     ;;Highlight 'TYPE'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|THEN\\|BEGIN\\|\;\\|ELSE\\>\\)\\s-*\\(\\<RETURN\\>\\)\\s-*\\(?:[-]?[0-9]+\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\(\\)"
     ;;Highlight 'RETURN'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<THEN\\|BEGIN\\|\\`\\|DO\\|\=\\|\;\\|ELSE\\>\\)\\s-*\\(\\<PROCEDURE\\>\\)\\s-*\\(?:[a-zA-Z][a-zA-Z0-9.\-]*\\)"
     ;;Highlight 'PROCEDURE'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<OF\\|\=\\|\:\\|\)\:\\)\\s-*\\(\\<PROCEDURE\\>\\)\\s-*\\(?:\(\\)"
     ;;Highlight 'PROCEDURE'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<OF\\|\=\\|\:\\|\)\:\\)\\s-*\\(\\<ARRAY\\>\\)\\s-*\\(?:\[\\)"
     ;;Highlight 'ARRAY'
     (1 'font-lock-keyword-face))
    ("\\(?:\]\\)\\s-*\\(\\<OF\\>\\)\\s-*\\(?:\\<INTEGER\\|ARRAY\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\[\\|PROCEDURE\\>\\)"
     ;;Highlight 'OF'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|THEN\\|BEGIN\\|\;\\|ELSE\\>\\)\\s-*\\(\\<WHILE\\>\\)\\s-*\\(?:[-]?[0-9]+\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\(\\)"
     ;;Highlight 'WHILE'
     (1 'font-lock-keyword-face))
    ("\\(?:[-]?[0-9]+\\|\]\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\)\\)\\s-*\\(\\<DO\\>\\)\\s-*\\(?:\\<DO\\|RETURN\\|THEN\\|ELSE\\|[-]?[0-9]+\\|WHILE\\|PRINT\\|VAR\\|PROCEDURE\\|IF\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\=\\|\;\\|\\`\\|TYPE\\|\(\\)"
     ;;Highlight 'DO'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|THEN\\|\]\\|\;\\|ELSE\\|[-]?[0-9]+\\|END\\|\)\\)\\s-*\\(\\<END\\>\\)\\s-*\\(?:\\<BEGIN\\|\;\\)"
     ;;Highlight 'END'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|THEN\\|\]\\|\;\\|ELSE\\|[-]?[0-9]+\\|END\\|\)\\)\\s-*\\(\\<END\\>\\)\\s-*\\(?:\\<END\\|\;\\|ELSE\\>\\)"
     ;;Highlight 'END'
     (1 'font-lock-keyword-face))
    ("\\(?:\\<DO\\|BEGIN\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|THEN\\|\]\\|\;\\|ELSE\\|[-]?[0-9]+\\|END\\|\)\\)\\s-*\\(\\<END\\>\\)\\s-*\\(?:\\'\\|END\\|\;\\|ELSE\\>\\)"
     ;;Highlight 'END'
     (1 'font-lock-keyword-face))
    ("\\(?:[-]?[0-9]+\\|\]\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\)\\)\\s-*\\(\\<AND\\>\\)\\s-*\\(?:[-]?[0-9]+\\|[a-zA-Z][a-zA-Z0-9.\-]*\\|\(\\)"
     ;;Highlight 'AND'
     (1 'font-lock-keyword-face))
    ("\\(?:[-]?[0-9]+\\)\\s-*\\(\\<TO\\>\\)\\s-*\\(?:[-]?[0-9]+\\)"
     ;;Highlight 'TO'
     (1 'font-lock-keyword-face))))
(defun mystery-mode ()
  (interactive)
  (kill-all-local-variables)
  (setq major-mode 'mystery-mode
        mode-name "mystery"
        fill-column 74
        indent-tabs-mode t
        tab-width 4)
  (set (make-local-variable 'require-final-newline) t)
  (set (make-local-variable 'next-line-add-newlines) nil)
  (set (make-local-variable 'font-lock-defaults)
       '(mystery-font-lock-keywords nil nil nil backward-paragraph (font-lock-lines-before . 2) (font-lock-lines-after . 2)))
  (set (make-local-variable 'font-lock-lines-before) 2))
