export function intersperse(ls, elt){
    return ls.flatMap(e => [elt, e]).slice(1)
}

export function intersperse_i(ls, generator){
    return ls.flatMap((e, i) => [generator(i), e]).slice(1);
}

export function updateToMatchLength(length, list, elementToAdd_generator){
    while (list.length < length){
        list.push(elementToAdd_generator());
    }

    list.splice(length, list.length-length);
    
}