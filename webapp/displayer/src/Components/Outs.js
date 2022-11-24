import Node from './Node';
import Selectable from './Selectable';

function InnerOuts(props){

    let {children} = props

    if (!children) return;

    if (!Array.isArray(props.children)) children = [children];


    let outs = props.x ? 
        children.map((out_, index) => <Node key={index}><div id={out_}/></Node>) :
        children.map((out_, index) => <Node key={index}>{out_}</Node>);
   
    return (outs);
}

const Outs = Selectable(InnerOuts);
export default Outs;