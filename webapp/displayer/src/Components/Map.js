import React from "react";
import { addProps } from "../Utils/ReactUtils";
import Movable from "./Movable";
import Selectable from "./Selectable";

function InnerMap(props){
    let {children, className, selected, fileinput, fileoutput, ...other} = props;
    let {infix, prefix, postfix} = props;
    let {inline} = props;
    
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
    
    if (props.name=='if'){
        ins = addProps(ins, {prefix:'t'});
        return (<table id={props.id} className={className} {...other}><tbody>
            <tr>
                <td>if</td>
                <td>{addProps(ins, {onlyShowIdx:0, name:'if'})}</td>
            </tr>
            <tr>
                <td>then</td>
                <td>{addProps(ins, {onlyShowIdx:1})}</td>
            </tr>
            <tr>
                <td>else</td>
                <td>{addProps(ins, {onlyShowIdx:2})}</td>
            </tr>
        </tbody></table>);
        
    }

    let map = <table id={props.id} className={className} {...other}><tbody>
        {ins}
        {infix || prefix || postfix? null : <tr><td>{props.name}</td></tr>}
        {outs}
    </tbody></table>

    if (inline)
        return map;

    return <div className="Node"> {map} </div>;
}

const Map = Movable(Selectable(InnerMap));
export default Map;