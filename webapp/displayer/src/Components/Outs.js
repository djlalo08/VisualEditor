import React from 'react';

export default function Outs(props){

    let {children} = props

    if (!children) return;

    if (!Array.isArray(props.children)) children = [children];


    let outs = props.x ? 
        children.map((out_, index) => <div key={index} id={out_}/>) :
        children.map((out_, index) => React.cloneElement(out_, {key: index}));
   
    return (outs);
}