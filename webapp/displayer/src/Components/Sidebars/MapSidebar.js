import React from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { updateAST } from '../../Actions';
import { updateToMatchLength } from '../../Utils/ListUtils';
import { addAttr, delAttr, makeNode } from '../../Utils/NodeUtils';

const positions = ['infix', 'postfix', 'underfix', 'prefix'];

export function MapSidebar({attrs, node}){

let [ins, outs] = node.children;
let {variableinput, inline} = attrs;

let onChangeInCount = e => {
    let newLength = e.target.value;
    console.log(newLength);
    updateToMatchLength(newLength, ins.children, () => makeNode(node));
    updateAST();
}

let onChangeOutCount = e => {
    let newLength = e.target.value;
    updateToMatchLength(newLength, outs.children, () => makeNode(node));
    updateAST();
}

let onChangeVisual = e => {
    delAttr(node, 'prefix');
    delAttr(node, 'infix');
    delAttr(node, 'postfix');
    delAttr(node, 'underfix');
    addAttr(node, e.target.value, 't');
    updateAST();
}

let onChangeInLine = e => {
    console.log(e.target.checked);
    if (e.target.checked)
        addAttr(node, 'inline', 't');
    else
        delAttr(node, 'inline');
    updateAST();
}
    

let insCount = ins.children.length;
let outsCount = outs && outs.children? outs.children.length: 0;

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
            onChange={onChangeInCount} disabled={!variableinput}/></Col>
    </Row>
    <Row>
      <Form.Label column>Outs</Form.Label>
      <Col><Form.Control type="number" value={outsCount} 
            onChange={onChangeOutCount}/></Col>
    </Row>
    <br/>
    <br/>
    <Row>
        <Form.Label column>Text Position</Form.Label>
        <Col> <Form.Select value={position} onChange={onChangeVisual}>
            <option value='underfix'>Underfix</option>
            <option value='prefix'>Prefix</option>
            <option value='infix'>Infix</option>
            <option value='postfix'>Postfix</option>
        </Form.Select> </Col>
    </Row>
    <Row>
        <Form.Label column>Inline</Form.Label>
        <Col> <Form.Check checked={inline || false} onChange={onChangeInLine} type="switch">
        </Form.Check> </Col>
    </Row>
</>;

}

//TODO line 83 needs to be a boolean option