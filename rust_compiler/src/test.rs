use std::{cell::RefCell, collections::HashMap, rc::Rc};

type Registry<I,T> = Rc<RefCell<HashMap<I,T>>>;

pub fn x(){
    let r: Registry<i32, String> = Rc::new(RefCell::new(HashMap::new()));
    r.borrow_mut().insert(3, String::from("Hello"));
    r.borrow_mut().insert(5, String::from("Hello"));
    add(Rc::clone(&r));
    add(Rc::clone(&r));
}

fn add(r: Registry<i32, String>){
    r.borrow_mut().insert(8, String::from("sss"));
}