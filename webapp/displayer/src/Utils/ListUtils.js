export function intersperse(ls, elt){
    return ls.flatMap(e => [elt, e]).slice(1)
}