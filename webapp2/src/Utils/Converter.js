import { Xwrapper } from "react-xarrows";
import { nextId, resetIds } from "../App";
import Block from "../Components/Block";
import Horizontal from '../Components/Horizontal';
import Ins from "../Components/Ins";
import Mapx from '../Components/Map';
import { MapDef } from "../Components/MapDef";
import Node from '../Components/Node';
import Outs from '../Components/Outs';
import Root from '../Components/Root';
import Vertical from '../Components/Vertical';
import Wire from '../Components/Wire';
import { getNameAndAttrs } from './NodeUtils';

function treeToJsx(node){
    let id = nextId() + '';
    let [nodeName, props]= getNameAndAttrs(node);

    props.id = id;
    props.ast_node = node;
    
    if (props['selected']) selected = node;
    
    let children = node.children.map(treeToJsx);
    
    switch (nodeName) {
        case 'Body':
        case 'Root':
            return <Root key={id} {...props}>{children}</Root>;
        case 'Vertical':
            return <Vertical key={id} {...props}>{children}</Vertical>;
        case 'Ins':
            return <Ins key={id} {...props}>{children}</Ins>;
        case 'Outs':
            return <Outs key={id} {...props}>{children}</Outs>;
        case 'Node':
            if (props.setvalue){
                if (wires_map[props.setvalue])
                    console.log(`multiple outs with value [${props.setvalue}]`);

                wires_map[props.setvalue] = [props.id, []];
            }
            if (props.getvalue){
                if (!wires_map[props.getvalue])
                    console.log(`The wire with value ${props.getvalue} is used but never assigned to`);

                wires_map[props.getvalue][1].push(props.id);
            }
            return <Node key={id} {...props}>{children}</Node>;
        case 'InBound':
            if (node.supplier)
                props.className += ' simulated ';
        case 'Variable':
        case 'UnBound':
            return <Block key={id} {...props}></Block>
        case 'MapDef':
            return <MapDef key={id} {...props}>{children}</MapDef>
        case 'Map':
            return <Mapx key={id} {...props}>{children}</Mapx>;
        case 'Horizontal':
            return <Horizontal key={id} {...props}>{children}</Horizontal>;
        default:
            return nodeName;
    }

}

function getWires(){
    let wires = [];
    for (let value in wires_map){
        let [start_id, end_ids] = wires_map[value];
        if (start_id && end_ids)
            for (let end_id of end_ids)
                wires.push(<Wire key={start_id+end_id} start={start_id} end={end_id}/>);
    }
    return wires;
}

export function ast_to_jsx(ast){
    clearGlobals(); 
    
    let jsx_root = treeToJsx(ast);
    let wires_ls = getWires();
    let children = [jsx_root, ...wires_ls];
    return [(<Xwrapper>{children}</Xwrapper>), selected];
}

let wires_map = {};
let selected = null;
let imports = {};

function clearGlobals(_setSelected){
    selected = null;
    wires_map = {};
    imports = {};
    resetIds();
}