import React from "react";
import { addProps } from "../Utils/ReactUtils";
import Movable from "./Movable";
import Selectable from "./Selectable";

function InnerMap(props){
    let {children, className, selected, fileinput, fileoutput, ...other} = props;
    
    let ins = children && children[0]? addProps(children[0], {...other}): [];
    let outs = children? children[1]: [];

    if (fileinput || fileoutput)
        className += ' io ';
    className += ' Map ';

    if (props.name=='id'){
        className += 'id';
        return (<table id={props.id} className={className} {...other}><tbody>
            {ins}
        </tbody></table>);
    }

    return (<table id={props.id} className={className} {...other}><tbody>
        {ins}
        {props.infix? null : <tr><td>{props.name}</td></tr>}
        {outs}
    </tbody></table>);
}

const Map = Movable(Selectable(InnerMap));
export default Map;