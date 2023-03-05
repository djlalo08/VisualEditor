import React from "react";
import { addProps } from "../Utils/ReactUtils";
import Movable from "./Movable";
import Selectable from "./Selectable";

function InnerMap(props){
    let {children, className, selected, ...other} = props;
    
    let ins = children && children[0]? addProps(children[0], {...other}): [];
    let outs = children? children[1]: [];

    return (<table id={props.id} className={props.className + " Map "} {...other}><tbody>
        {ins}
        {props.infix? null : <tr><td>{props.name}</td></tr>}
        {outs}
    </tbody></table>);
}

const Map = Movable(Selectable(InnerMap));
export default Map;