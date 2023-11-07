export function n_tabs(n) {
    let tabs = '';
    for (let i = 0; i < n; i++) {
        tabs += '    ';
    }
    return tabs;
}

export function indent_level(str){
    let level = 0;
    while (str.startsWith('    ')){
        str = str.slice(4);
        level += 1;
    }
    return level;
}