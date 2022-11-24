import React from 'react';
import { intersperse } from '../Utils/ListUtils';
import Node from './Node';

export default function Ins(props){
   
let {children, infix, ...other} = props

    if (!children) return;

    if (!Array.isArray(props.children)) children = [children];

    let ins = props.x ?
        children.map((in_, index) => <Node key={index} {...other}><div id={in_}/></Node>):
        children.map((in_, index) => <Node key={index} {...other}>{in_}</Node>);

    if (infix) ins = intersperse(ins, props.name);
    
    return (ins);
}