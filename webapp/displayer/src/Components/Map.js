import React from "react";


export default function Map(props){
    let {children, ...other} = props;
    
    let ins = children? children[0]: [];
    let ins2 = React.Children.map(ins, x => React.cloneElement(x, {...other}));
    let outs = children? children[1]: [];

    const makeCall = async () => {
        const response = await fetch(`http://localhost:5000/select/${props.id}`);
        const text = await response.text(); 
        alert(text)
    }

    let on_click = (e) => {
        e.stopPropagation();
        makeCall();
    }
    
    return (<div id={props.id} className={props.className || "Map"} onClick={on_click}>
        {ins2}
        {props.infix? <br/> : <div>{props.name}</div>}
        {outs}
    </div>);
}
