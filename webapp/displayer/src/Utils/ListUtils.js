export function intersperse(ls, elt){
    return ls.flatMap(e => [elt, e]).slice(1)
}

export function intersperse_i(ls, generator){
    return ls.flatMap((e, i) => [generator(i), e]).slice(1);
}