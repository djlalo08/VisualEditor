import React, { useState } from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { updateAST } from '../../Actions';
import { addAttr } from '../../Utils/NodeUtils';

export function ConstantSidebar({attrs, node}){

const [nameInTextbox, setNameInTextbox] = useState('');

let {isnamed, value} = attrs;
isnamed = isnamed === 'true';

let onChangeValue = e => {
    let newValue = e.target.value;
    addAttr(node, 'value', newValue);
    if (!isnamed) addAttr(node, 'name', newValue);
    updateAST();
}

let onChangeIsNamed = e => {
    let newValue = e.target.checked;
    addAttr(node, 'isnamed', newValue);
    if (newValue)
        addAttr(node, 'name', nameInTextbox); 
    else
        addAttr(node, 'name', value); 
    updateAST();
}

let onChangeName = e => {
    let newValue = e.target.value;
    setNameInTextbox(newValue);
    addAttr(node, 'name', newValue);
    updateAST();
}

return <>
    <Row>
      <Form.Label column>Named Constant</Form.Label>
      <Col><Form.Check type="switch" value={isnamed} 
            onChange={onChangeIsNamed}/></Col>
      <Col><Form.Control type="text" disabled={!isnamed} 
            onChange={onChangeName} value={nameInTextbox}/></Col>
    </Row>
    <Row>
      <Form.Label column>Value</Form.Label>
      <Col><Form.Control type="number" value={value} 
            onChange={onChangeValue}/></Col>
    </Row>
</>;

}