# POO 💩

POO is general purpose, strongly typed, functional, homoiconic visual programming language.

There are many ideas packed into this language, so feel free to explore!

### How it works 

Code in the POO editor is represented by maps that have input and output nodes, and wires that connect them. This view largely inspired by LabView (a language I hate), but avoiding many of its major downfalls (cluttered code, confusing control, bad complexity management, too much hassle worrying about wire management and box placement, heavy-weight proprietary editor). However, I contend that functional programming is actually very well suited for LabView-style visual display as chains of operations affecting data. One of the goals of POO is to visually capture the intuition of functional programming.

The full specification of any program is determined in the Intermediate Representation (IR). While much of my efforts are currently focused on the editor, and trying to understand what is really possible with it, the editor itself is not POO. The IR is at the heart of POO, and it is also quite simple, but has many valuable properties. Most importantly, the IR has a one-to-one correspondence with what is seen in the editor, and can also be either directly run by the editor, or compiled into machine code. 


### Some features of POO

- **Contextual**: POO is a contextual language. This means that the source code contains an abundance of information, but that information is shown contextually as desired. This can allow for very powerful clarity and specificity in code, without adding clutter or noise to the code reading/writing experience. This kind of contextual information, for example, can allow for a very deep and rich type system, which would otherwise be nightmare-ish to handle and represent.

- **Homoiconic**: The IR is fully homoiconic. This means that code in POO is also data in POO. This further means that the language is highly extensible, much as lisps are -- features can be added to POO within POO. The difference between adding new features to a lisp and POO is that in a lisp, lisp code is sufficient to extend the language. In many cases, this is also true of POO, but if a user wishes to create new visual representations of language extensions in POO, then they must also extend the editor for those change to be visible. This is why the editor is also designed to be highly extensible. (Of course it is possible to extend the language exclusively within POO, but then any new features created must depend on existing editor elements -- this would be similar to the way that in most cases, lisp macros are still depicted as function calls).

- **Predicate Typing**: Possible inputs into a given function can be very complex thanks to predicate typing. For example, we can make a function that takes only even digits as input. This kind of precise specification, can give us compile-time guarantees about the data in our program and allow automated testing that captures a wide range of possibilities

- **Portable**: Even though POO is a visual language intended to be written and read in an editor that follows the POO spec (the IR is sort of human-readable, but writing in IR directly is a guaranteed bad time), every piece of POO code is fundamentally represented in the IR, which is a simple plain-text document. This means POO code can be shared and moved without fear of data corruption. Building the editor into a webapp also means that POO is accessible to anyone with a modern browser and internet connection. IR can also be compiled into machine-executable code, which means that computers without a POO compiler can run POO programs.

- **Readable**: The human visual cortex is an immensely powerful system, and text-based languages can fail to capitalize on that. POO makes extremely obvious the connections between different pieces of data and where everything in the code is coming from. POO's functional-first design makes many functional ideas come to life and make obvious, intuitive sense. It is also very helpful in various situations, such as async/parallel/multi-threaded code.


### How To Install POO

This repo contains various experiments and explorations that have been valuable in the design and test of POO. The most recent, and currently active work can be found under webapp/displayer. This app is not yet hosted anywhere, so in order to try using it, You must run it locally: 
1) Clone this repo to a local directory on Your machine
2) Make sure You have [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed
3) In a terminal, navigate to VisualEditor/webapp/displayer
4) Run the following command in terminal: run npm
5) Previous step should automatically open a browser window with the webapp. If it does not, webapp can be found by typing localhost:3000 into browser address bar 

You can also explore some different Python, Java, and Closure-based implementations I have in the various subdirectories of this repo. 

### How To Use POO

Note: This section is pending improvment.
Here is a list of commands available in the webapp (note some migh tbe in development or bugged at the time of reading): 

Navigation:
- Left mouse-click: Select a node
- Arrow keys left/right (←→): Move selection to next or previous component at current level (horizontal navigation)
- Arrow keys up/down (↑↓): Move selection to parent or child component (depth navigation)
- Enter: Move to next line (vertical navigation)
- Shift+Enter: Move to previous line (vertical navigation)

Insertion/Deletion:
- Space: Insert map at current selection. New map become child of current selection(depth insertion)
- Shift+Space: Wrap current  node with map. New map become parent of current selection (depth insertion)
- W: Insert map above current selection (vertical insertion)
- S: Insert map below current selection (vertical insertion)
- A: Insert map to the left of current selection (horizontal insertion)
- D: Insert map to the right of current selection (horizontal insertion)
- Backspace/Delete: Delete selected element

Selection Modes:
- T: Second selection mode
- M: Move second selection into selection
- E: Extract selected node, moving it outside of current context
- C: Connect wires

Other:
- Z: Undo
- Shift+Z: Redo

Buttons:
- Print AST: Will print the AST corresponding to the current code in editor in the browser console. This should be virtually identical to the IR
- Open file: Loads a fixed file into editor. Typically not necessary to call
- Save: Saves current open editor as a new file, downloaded to browser
- Eval: Evaluates the current selection, printing the resulting value at the bottom of the screen
- FileStuff: Grants browser access to selected directory. This allows editor to read IRs that may be located in select dir, and enable to import them

Some insertion commands produce a pop-up to type into. In these cases, type the name of the map desired, and then hit Enter.
Some elements have an associated sidebar that appears when they are selected. Modifying the options on the sidebar, will effect changes in the corresponding element



