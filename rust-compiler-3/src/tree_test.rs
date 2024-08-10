pub fn trees() {
    let mut root = 
    Node {
        children: vec![
            Node {
                children: vec![],
                value: 3,
                sum: 0,
            },
            Node {
                children: vec![
                    Node {
                        children: vec![ ],
                        value: 1,
                        sum: 0,
                    },
                    Node {
                        children: vec![ ],
                        value: 2,
                        sum: 0,
                    },
                ],
                value: 3,
                sum: 0,
            },
            Node {
                children: vec![
                    Node {
                        children: vec![ ],
                        value: 6,
                        sum: 0,
                    },
                ],
                value: 12,
                sum: 0,
            },

        ],
        value: 3,
        sum: 0,
    };

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
}