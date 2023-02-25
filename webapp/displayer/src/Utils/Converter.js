import { Xwrapper } from "react-xarrows";
import FileInput from "../Components/FileInput";
import FileOutput from "../Components/FileOutput";
import GenericNode from "../Components/GenericNode";
import Horizontal from '../Components/Horizontal';
import Ins from "../Components/Ins";
import Mapx from '../Components/Map';
import Node from '../Components/Node';
import Outs from '../Components/Outs';
import Root from '../Components/Root';
import Vertical from '../Components/Vertical';
import Wire from '../Components/Wire';

export default function ir_to_components(ir_text) {
    let tree = parse(ir_text);
}

function readAttrs(attrStr){
    let attrs = {};
    if (!attrStr) return attrs;

    for (let attr of attrStr.split(',')){
        let attrPair = attr.trim().split(':');
        attrs[attrPair[0]] = attrPair[1];
    }
    return attrs;
}

function treeToJsx(tree, key){
    let id = ++id_gen + '';
    let values = tree.value.split(/[\[\]]/);
    let nodeName = values[0];
    let attrs = readAttrs(values[1]);
    attrs["id"] = id;
    let children = [];

    for (let [i, child] of tree.children.entries()){
        children.push(treeToJsx(child, i));
    }
    
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
            console.log(attrs);
            return <Mapx {...attrs}>{children}</Mapx>;
        case 'Horizontal':
            return <Horizontal {...attrs}>{children}</Horizontal>;
        case 'FileInput':
            return <FileInput {...attrs}>{children}</FileInput>;
        case 'FileOutput':
            return <FileOutput {...attrs}>{children}</FileOutput>;
        case 'SetNode':
            console.log(attrs);
            if (! wires_map[attrs['value']])
                wires_map[attrs['value']] = [-1,-1];

            wires_map[attrs['value']][0] = id;
            // return id;
            return <div id={id}/>;
        case 'GetNode':
            if (! wires_map[attrs['value']])
                wires_map[attrs['value']] = [-1,-1];

            wires_map[attrs['value']][1] = id;
            return <div id={id}/>;
        default:
            return genericNode(nodeName, key, children);
    }

}

function genericNode(nodeName, key, children, style){
    return (<GenericNode nodeName={nodeName} key={key}>
        {children} 
    </GenericNode>);
}

function parse(ir_text){
    let lines = ir_text.split("\n");
    let last_indent = 0;
    let root_node = {value: "", children: [], parent: {children: []}};
    let last_node = root_node;
    for (let line of lines) {
        let indent = line.search(/\S/)/4;

        let parent_to_the_node_we_are_adding = last_node;
        for (let i = 0; i <= last_indent-indent; i++){
            parent_to_the_node_we_are_adding = parent_to_the_node_we_are_adding.parent;
        }

        let this_node = {value: line.trim(), children: [], parent: parent_to_the_node_we_are_adding};

        parent_to_the_node_we_are_adding.children.push(this_node);

        last_node = this_node; 
        last_indent = indent;
    };
    return root_node.parent.children[0];
}

function getWires(){
    let wires = [];
    for (let value in wires_map){
        let [start_id, end_id] = wires_map[value];
        wires.push(<Wire start={start_id} end={end_id}/>);
    }
    return wires;
}

export function run_parse(){
    clearGlobals(); 
    
    let parsed = parse(ex);
    let jsx_root = treeToJsx(parsed);
    let wires_ls = getWires();
    console.log(wires_ls);
    console.log(wires_map);
    let children = [jsx_root, ...wires_ls];
    return (<Xwrapper>{children}</Xwrapper>);
}

let wires_map = {};
let id_gen = 0;

function clearGlobals(){
    wires_map = {};
    id_gen = 0;
}

const ex = `Root
    Horizontal
        FileInput
            SetNode[value:a, x:True]
        FileInput
            SetNode[value:b, x:True]
        FileInput
            SetNode[value:c, x:True]
    Vertical
        Map[name:sqrt]
            Ins
                Node
                    Map[name:-, infix:true]
                        Ins[infix:true]
                            Node
                                Map[name:sqr]
                                    Ins
                                        Node
                                            GetNode[value:b]
                                    Outs
                            Node
                                Map[name:*, infix:true]
                                    Ins[infix:true]
                                        Node
                                            Map[name:4, className:constant, selected:' ']
                                        Node
                                            GetNode[value:a]
                                        Node
                                            GetNode[value:c]
                                    Outs[infix:true]
                        Outs[infix:true]
            Outs
                Node
                    SetNode[value:discr]
    Horizontal
        FileOutput
            GetNode[value:discr, x:True]`