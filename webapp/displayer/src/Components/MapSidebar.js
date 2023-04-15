import React from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { updateAST } from '../Actions';

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
    
    
let insCount = ins.children.length;
let outsCount = outs.children.length;

return <>
    <Row>
      <Form.Label column htmlFor="exampleColorInput">Ins</Form.Label>
      <Col><Form.Control type="number" value={insCount} 
            onChange={onChangeInCount}/></Col>
    </Row>
    <Row>
      <Form.Label column htmlFor="exampleColorInput">Outs</Form.Label>
      <Col><Form.Control type="number" value={outsCount} 
            onChange={onChangeOutCount}/></Col>
    </Row>
    <br/>
    <br/>
    <Row>
      <Form.Label column htmlFor="exampleColorInput">Visual</Form.Label>
      <Col><Form.Control type="number" value={outsCount} 
            onChange={onChangeOutCount}/></Col>
    </Row>
</>;

}
