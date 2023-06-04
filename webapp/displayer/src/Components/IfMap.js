import React from "react";
import { addProps } from "../Utils/ReactUtils";

export function IfMap(props){
    let {id, className, ins, other} = props;
    let newIns = addProps(ins, {prefix:'t'}) ;
    return (<table id={id} className={className} {...other}><tbody>
        <tr>
            <td>if</td>
            <td>{addProps(newIns, {onlyShowIdx:0, name:'if'})}</td>
        </tr>
        <tr>
            <td>then</td>
            <td>{addProps(newIns, {onlyShowIdx:1})}</td>
        </tr>
        <tr>
            <td>else</td>
            <td>{addProps(newIns, {onlyShowIdx:2})}</td>
        </tr>
    </tbody></table>);
    
}