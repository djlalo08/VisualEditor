import React from "react";
import Movable from "./Movable";
import Selectable from "./Selectable";

function InnerBlock(props){
    let {className, selected, ...other} = props;
    
    className += ' Map ';

    return (<table id={props.id} className={className} {...other}><tbody>
        <tr><td>{props.name}</td></tr>
    </tbody></table>);
}

const Block = Movable(Selectable(InnerBlock));
export default Block;