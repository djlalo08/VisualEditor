import Node from './Node';

export default function Ins(props){

    let {children} = props

    if (!children) return;

    if (!Array.isArray(props.children)) children = [children];

    let outs = children.map((out_, index) => <Node key={index}>{out_}</Node>);
   
    return (outs);
}