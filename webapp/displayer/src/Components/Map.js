import React from "react";
import Movable from "./Movable";
import Selectable from "./Selectable";

function InnerMap(props){
    let {children, className, selected, ...other} = props;
    
    let ins = children? children[0]: [];
    let ins2 = React.Children.map(ins, x => React.cloneElement(x, {...other}));
    let outs = children? children[1]: [];

    return (<div id={props.id} className={props.className + " Map "} {...other}>
        {ins2}
        {props.infix? <br/> : <div>{props.name}</div>}
        {outs}
    </div>);
}

const Map = Movable(Selectable(InnerMap));
export default Map;