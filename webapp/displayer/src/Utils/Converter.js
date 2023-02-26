import { Xwrapper } from "react-xarrows";
import FileInput from "../Components/FileInput";
import FileOutput from "../Components/FileOutput";
import Horizontal from '../Components/Horizontal';
import Ins from "../Components/Ins";
import Mapx from '../Components/Map';
import Node from '../Components/Node';
import Outs from '../Components/Outs';
import Root from '../Components/Root';
import Vertical from '../Components/Vertical';
import Wire from '../Components/Wire';
import { getNameAndAttrs } from './NodeUtils';


function treeToJsx(tree){
    let id = ++id_gen + '';

    let [nodeName, props]= getNameAndAttrs(tree.value);
    props.id = id;
    props.key = id;
    props.ast_node = tree;
    
    if (props['selected']) selected = tree;
    
    let children = tree.children.map(treeToJsx);
    
    switch (nodeName) {
        case 'Root':
            return <Root {...props}>{children}</Root>;
        case 'Vertical':
            return <Vertical {...props}>{children}</Vertical>;
        case 'Ins':
            return <Ins {...props}>{children}</Ins>;
        case 'Outs':
            return <Outs {...props}>{children}</Outs>;
        case 'Node':
            return <Node {...props}>{children}</Node>;
        case 'Map':
            return <Mapx {...props}>{children}</Mapx>;
        case 'Horizontal':
            return <Horizontal {...props}>{children}</Horizontal>;
        case 'FileInput':
            return <FileInput {...props}>{children}</FileInput>;
        case 'FileOutput':
            return <FileOutput {...props}>{children}</FileOutput>;
        case 'SetNode':
            if (! wires_map[props.value])
                wires_map[props.value] = [-1,-1];

            wires_map[props.value][0] = id;
            return <div {...props}/>;
        case 'GetNode':
            if (! wires_map[props.value])
                wires_map[props.value] = [-1,-1];

            wires_map[props.value][1] = id;
            return <div {...props}/>;
        default:
            return nodeName;
    }

}

function getWires(){
    let wires = [];
    for (let value in wires_map){
        let [start_id, end_id] = wires_map[value];
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
let id_gen = 0;
let selected = null;

function clearGlobals(_setSelected){
    selected = null;
    wires_map = {};
    id_gen = 0;
}