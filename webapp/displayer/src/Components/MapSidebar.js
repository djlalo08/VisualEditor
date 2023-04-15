import React from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { updateAST } from '../Actions';
import { addAttr, delAttr } from '../Utils/NodeUtils';

const positions = ['infix', 'postfix', 'underfix', 'prefix'];

export function MapSidebar({attrs, node}){

let [ins, outs] = node.children;

let onChangeInCount = e => {
    let newValue = e.target.value;
    if (newValue > ins.children.length){
        ins.children.push({value:'Node', parent:node, children:[]});
        updateAST();
    }
}

let onChangeOutCount = e => {
    let newValue = e.target.value;
    if (newValue > outs.children.length){
        outs.children.push({value:'Node', parent:node, children:[]});
        updateAST();
    }
}

let onChangeVisual = e => {
    delAttr(node, 'prefix');
    delAttr(node, 'infix');
    delAttr(node, 'postfix');
    delAttr(node, 'underfix');
    addAttr(node, e.target.value, 't');
    updateAST();
}
    
    
let insCount = ins.children.length;
let outsCount = outs.children.length;

let position = 'underfix';
for (let p of positions){
    if (p in attrs){
        position = p;
        break;
    }
}

return <>
    <Row>
      <Form.Label column>Ins</Form.Label>
      <Col><Form.Control type="number" value={insCount} 
            onChange={onChangeInCount}/></Col>
    </Row>
    <Row>
      <Form.Label column>Outs</Form.Label>
      <Col><Form.Control type="number" value={outsCount} 
            onChange={onChangeOutCount}/></Col>
    </Row>
    <br/>
    <br/>
    <Row>
        <Form.Label column>Visual</Form.Label>
        <Col> <Form.Select value={position} onChange={onChangeVisual}>
            <option value='underfix'>Underfix</option>
            <option value='prefix'>Prefix</option>
            <option value='infix'>Infix</option>
            <option value='postfix'>Postfix</option>
        </Form.Select> </Col>
    </Row>
</>;

}
