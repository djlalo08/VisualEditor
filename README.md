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

- Readable: The human visual cortex is an immensely complex and powerful system, and text-based languages can fail to capitalize on that. POO makes extremely obvious the connections between different pieces of data and where everything in the code is coming from. POO's functional-first design makes many functional ideas come to life and make obvious sense. It is also very helpful in various situations, such as async/parallel/multi-threaded code.
