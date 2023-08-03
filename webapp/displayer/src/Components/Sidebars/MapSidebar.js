import React from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { setMapIns, updateAST } from '../../Actions';
import { updateToMatchLength } from '../../Utils/ListUtils';
import { addAttr, delAttr, makeNode } from '../../Utils/NodeUtils';

const positions = ['infix', 'postfix', 'underfix', 'prefix'];

export function MapSidebar({attrs, node}){

let [ins, outs] = node.children;
let {variableinput, inline} = attrs;
let {hide_outs, returnidx} = attrs;

let onChangeInCount = e => {
    setMapIns(node, e.target.value);
}

let onChangeOutCount = e => {
    let newLength = e.target.value;
    updateToMatchLength(newLength, outs.children, () => makeNode(outs));
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
    if (e.target.checked)
        addAttr(node, 'inline', 't');
    else
        delAttr(node, 'inline');
    updateAST();
}

let onChangeHideOuts = e => {
    if (e.target.checked)
        addAttr(node, 'hide_outs', 't');
    else
        delAttr(node, 'hide_outs');
        delAttr(node, 'returnidx');
    updateAST();
}

let onChangeReturnIdx = e => {
    let newIdx = e.target.value;
    addAttr(node, 'returnidx', newIdx);
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
            onChange={onChangeInCount} disabled={!variableinput} min={0}/></Col>
    </Row>
    <Row>
      <Form.Label column>Outs</Form.Label>
      <Col><Form.Control type="number" value={outsCount} 
            onChange={onChangeOutCount} min={0}/></Col>
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
        </Form.Check></Col>
    </Row>
    <Row>
        <Form.Label column>HideOuts</Form.Label>
        <Col> <Form.Check checked={hide_outs || false} onChange={onChangeHideOuts} type="switch">
        </Form.Check></Col>
        <Form.Label column>ReturnIdx</Form.Label>
        <Col><Form.Control type="number" disabled={!hide_outs} 
            onChange={onChangeReturnIdx} value={!hide_outs? '': returnidx} max={outsCount-1} min={0}/></Col>
    </Row>

</>;

}