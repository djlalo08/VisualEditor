import React from "react";
import { addProps } from "../Utils/ReactUtils";
import { IfMap } from "./IfMap";
import Movable from "./Movable";
import Selectable from "./Selectable";

function InnerMap(props){
    let {children, className, selected, fileinput, fileoutput, ...other} = props;
    let {infix, prefix, postfix} = props;
    let {inline, hide_outs} = props;
    
    let ins = children && children[0]? addProps(children[0], {...other}): [];
    let outs = children? children[1]: [];

    if (fileinput || fileoutput)
        className += ' io ';
    className += ' Map ';
    className += props.recursive? ' Recursive ' : '';

    if (props.name=='id'){
        className += 'id';
        return (<table id={props.id} className={className} {...other}><tbody>
            {ins}
        </tbody></table>);
    }

    let map = <table id={props.id} className={className} {...other}><tbody>
        {ins}
        {infix || prefix || postfix? null : <tr><td>{props.name}</td></tr>}
        <tr style={{height:'4px'}}><td></td></tr>
        {hide_outs? null: outs}
    </tbody></table>
    
    if (props.name=='if')
        map = <IfMap {...props} other={other} ins={ins}/>;

    if (inline)
        return map;

    return <div className="Node"> {map} </div>;
}

const Map = Movable(Selectable(InnerMap));
export default Map;