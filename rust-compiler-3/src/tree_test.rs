pub fn trees() {
    let mut root = 
    Node::new(3, 1, 0, vec![
        Node::new(3, 2, 1, vec![]),
        Node::new(3, 3, 1, vec![
            Node::new(1, 4, 3, vec![]),
            Node::new(2, 5, 3, vec![]),
        ]),
        Node::new(12, 6, 1, vec![
            Node::new(6, 7, 6, vec![]),
        ]),
    ]);

    println!("{:#?}", root);
    update_sums(&mut root);
    println!("{:#?}", root);

}

fn update_sums(root: &mut Node){
    root.children.iter_mut().for_each(|n| update_sums(n));
    root.sum = root.children.iter()
        .map(|n| n.sum)
        .fold(root.value, |acc, x| acc+x);
}

#[derive(Debug)]
struct Node {
   children: Vec<Node>,
   value: i32,
   sum: i32,
   id: i32,
   par_id: i32,
}

impl Node {
    fn new(value: i32, id: i32, par_id: i32, children: Vec<Node>) -> Self{
        Node {
            children,
            value,
            sum: 0,
            id,
            par_id,
        }
    }


}
