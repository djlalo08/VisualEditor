Project has been updated to focus on JS front-end rendering (much easier and cleaner than PyCharm) and editing IRs (intermediate representations). The general idea is that IR is a plain-text file that is one-to-one with evaluated code and also one-to-one with UI. This means everything is explicitly defined and also we can separate out front-end representation and backend compilation entirely. IR is also homoiconic which will enable powerful LISP-like macros (read "making an IR homoiconic for more depth on the matter).

Main project is in webapp/displayer
