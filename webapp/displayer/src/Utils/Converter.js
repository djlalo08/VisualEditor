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

function readAttrs(attrStr){
    let attrs = {};
    if (!attrStr) return attrs;

    for (let attr of attrStr.split(',')){
        let attrPair = attr.trim().split(':');
        attrs[attrPair[0]] = attrPair[1];
    }
    return attrs;
}

function treeToJsx(tree){
    let id = ++id_gen + '';

    let values = tree.value.split(/[\[\]]/);
    let nodeName = values[0];

    let attrs = readAttrs(values[1]);
    attrs.id = id;
    attrs.key = id;

    let children = tree.children.map(treeToJsx);
    
    switch (nodeName) {
        case 'Root':
            return <Root {...attrs}>{children}</Root>;
        case 'Vertical':
            return <Vertical {...attrs}>{children}</Vertical>;
        case 'Ins':
            return <Ins {...attrs}>{children}</Ins>;
        case 'Outs':
            return <Outs {...attrs}>{children}</Outs>;
        case 'Node':
            return <Node {...attrs}>{children}</Node>;
        case 'Map':
            return <Mapx {...attrs}>{children}</Mapx>;
        case 'Horizontal':
            return <Horizontal {...attrs}>{children}</Horizontal>;
        case 'FileInput':
            return <FileInput {...attrs}>{children}</FileInput>;
        case 'FileOutput':
            return <FileOutput {...attrs}>{children}</FileOutput>;
        case 'SetNode':
            if (! wires_map[attrs.value])
                wires_map[attrs.value] = [-1,-1];

            wires_map[attrs.value][0] = id;
            return <div {...attrs}/>;
        case 'GetNode':
            if (! wires_map[attrs.value])
                wires_map[attrs.value] = [-1,-1];

            wires_map[attrs.value][1] = id;
            return <div {...attrs}/>;
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
    return (<Xwrapper>{children}</Xwrapper>);
}

let wires_map = {};
let id_gen = 0;

function clearGlobals(){
    wires_map = {};
    id_gen = 0;
}