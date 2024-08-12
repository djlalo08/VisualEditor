use std::{cell::RefCell, rc::{Rc, Weak}};

pub fn fn4() {

}

struct Node {
    children: Vec<Rc<RefCell<Node>>>,
    parent: Option<Weak<Node>>,
    value: String,
}

impl Node {
    fn new(val: &str, parent: Option<Weak<Node>>) -> Node {
        Node {
            children: vec![],
            parent,
            value: val.to_string(),
        }
    }

    fn add_child(self: Rc<RefCell<Self>>, child: Node) {

        self.children.push(Rc::new(child));
        child.parent = Some(Rc::downgrade(&self));
    } 
}