import { Xwrapper } from "react-xarrows";
import { loadImports as loadImportsAction } from "../Actions";
import { nextId, resetIds } from "../App";
import Block from "../Components/Block";
import Horizontal from '../Components/Horizontal';
import Ins from "../Components/Ins";
import Mapx from '../Components/Map';
import Node from '../Components/Node';
import Outs from '../Components/Outs';
import Root from '../Components/Root';
import Vertical from '../Components/Vertical';
import Wire from '../Components/Wire';
import { getImports, getNameAndAttrs } from './NodeUtils';


function treeToJsx(node){
    let id = nextId() + '';
    let [nodeName, props]= getNameAndAttrs(node);

    props.id = id;
    props.key = id;
    props.ast_node = node;
    
    if (props['selected']) selected = node;
    
    let children = node.children.map(treeToJsx);
    
    switch (nodeName) {
        case 'Root':
            return <Root {...props}>{children}</Root>;
        case 'Vertical':
            return <Node {...props}><Vertical {...props}>{children}</Vertical></Node>;
        case 'Ins':
            return <Ins {...props}>{children}</Ins>;
        case 'Outs':
            return <Outs {...props}>{children}</Outs>;
        case 'OutBinding':
        case 'InBinding':
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
            return <Node {...props}>{children}</Node>;
        case 'InBound':
            if (node.supplier)
                props.className += ' simulated ';
        case 'Variable':
        case 'Constant':
        case 'UnBound':
        case 'OutBound':
            return <Block {...props}></Block>
        case 'Map':
            return <Mapx {...props}>{children}</Mapx>;
        case 'Horizontal':
            return <Horizontal {...props}>{children}</Horizontal>;
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

export function loadImports(root){
    loadImportsAction(getImports(root));
}

export function ast_to_jsx(ast){
    clearGlobals(); 
    
    loadImports(ast);
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