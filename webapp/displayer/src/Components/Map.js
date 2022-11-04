import React from "react";


export default function Map(props){
    let {children, ...other} = props;
    
    let ins = children? children[0]: [];
    let ins2 = React.Children.map(ins, x => React.cloneElement(x, {...other}));
    let outs = children? children[1]: [];

    let on_click = (e) => {
        e.stopPropagation();
        alert(props.name);
    }
    
    return (<div id={props.id} className={props.className || "Map"} onClick={on_click}>
        {ins2}
        {props.infix? <br/> : <div>{props.name}</div>}
        {outs}
    </div>);
}
