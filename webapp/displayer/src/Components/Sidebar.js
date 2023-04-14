import React from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Row from 'react-bootstrap/Row';
import { updateAST } from '../Actions';
import { getNameAndAttrs } from '../Utils/NodeUtils';

export function Sidebar({node}) {
    if (!node)
        return;

    let [name, attrs]  = getNameAndAttrs(node);
    
    return (
        <Offcanvas show={true} scroll={true} backdrop={false} placement='end'>
            <Offcanvas.Header>
                <Offcanvas.Title>{name}: {attrs.name}</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
                {body(name, attrs, node)}
            </Offcanvas.Body>
        </Offcanvas>
    );
}

function body(name, attrs, node){
    let onChangeInCount = e => {
        let [ins, outs] = node.children;
        let newValue = e.target.value;
        console.log(ins);
        if (newValue > ins.children.length){
            ins.children.push({value:'Node', parent:node, children:[]});
            updateAST();
        }
    }

    switch(name){
        case 'Map':
            let [ins, outs] = node.children;
            let insCount = ins.length;
            return <>
                <Row>
                  <Form.Label column htmlFor="exampleColorInput">Ins</Form.Label>
                  <Col><Form.Control 
                        type="number"
                        value={insCount} 
                        onChange={onChangeInCount}/></Col>
                </Row>
                <Row>
                  <Form.Label column htmlFor="exampleColorInput">Outs</Form.Label>
                  <Col><Form.Control type="number" /></Col>
                </Row>
            </>;
    }
}
