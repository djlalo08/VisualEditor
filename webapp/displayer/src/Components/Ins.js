import React from 'react';
import { intersperse } from '../Utils/ListUtils';

export default function Ins(props){
   
let {children, infix} = props

    if (!children) return;

    if (!Array.isArray(props.children)) children = [children];

    let ins = props.x ?
        children.map((in_, index) => <div key={index} id={in_}/>):
        children.map((in_, index) => React.cloneElement(in_, {key: index}));

    if (infix) ins = intersperse(ins, props.name);
    
    return (ins);
}