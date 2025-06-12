#[macro_export]
macro_rules! log {
    ($m:expr) => {
        log!($m,);
    };
    ($m:expr, $($args:expr),*) => {
        log!(0; $m, $($args),*);
    };
    ($depth:expr; $m:expr, $($args:expr),*) => {
        let mut file = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open("log.txt")
            .unwrap();
        writeln!(file, "{}{}", $crate::utils::tab($depth), format!($m, $($args),*)).unwrap();
    };
}

pub fn tab(n: usize) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push(' ');
        s.push('┃');
        s.push(' ');
    }
    s
}
