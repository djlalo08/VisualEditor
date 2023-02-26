import React from "react";
import Selectable from "./Selectable";

function InnerMap(props){
    let {children, className, selected, ast_node, ...other} = props;
    
    let ins = children? children[0]: [];
    let ins2 = React.Children.map(ins, x => React.cloneElement(x, {...other}));
    let outs = children? children[1]: [];

    let on_click = (e) => {
        e.stopPropagation();
        props.select_fn(ast_node);
    }
    
    return (<div id={props.id} className={props.className + " Map"} onClick={on_click}>
        {ins2}
        {props.infix? <br/> : <div>{props.name}</div>}
        {outs}
    </div>);
}

const Map = Selectable(InnerMap);
export default Map;