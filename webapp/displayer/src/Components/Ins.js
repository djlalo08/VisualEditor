import React from 'react';
import { intersperse } from '../Utils/ListUtils';
import Node from './Node';

export default function Ins(props){
   
    let {children, infix} = props

    if (!children) return;

    if (!Array.isArray(props.children)) children = [children];

    let ins = children.map((in_, index) => <Node key={index}>{in_}</Node>);

    if (infix) ins = intersperse(ins, props.name);
    
    return (ins);
}