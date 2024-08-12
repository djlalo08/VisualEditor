use indextree::Arena;

pub fn trees(){
    let arena = &mut Arena::new();
    
    let a = arena.new_node(MyData::default());
    let b = arena.new_node(MyData::default());
    let c = arena.new_node(MyData::default());

    a.append(b, arena); 
    a.append(c, arena); 

    
    let mut z = arena.get_mut(b).unwrap().get_mut();
    z.a = 24;
    
    println!("{:#?}", arena);
}

#[derive(Debug)]
struct MyData {
    a: i32,
    b: Vec<i32>,
    c: i32,
}

impl MyData {
    fn default() -> Self {
        MyData {
            a: 0, 
            b: vec![],
            c: 0,
        }
    }
}