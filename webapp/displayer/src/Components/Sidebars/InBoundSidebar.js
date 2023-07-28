import React from 'react';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { updateAST } from '../../Actions';
import { getAttrs, getInBounds } from '../../Utils/NodeUtils';

export function InBoundSidebar({attrs, node, AST}){

let {bind_idx} = attrs;
let inBounds = getInBounds(AST);

let onChangeValue = e => {
    let newValue = e.target.value;
    for (let inBound of inBounds){
        if (getAttrs(inBound).bind_idx == bind_idx)
            inBound.supplier = () => newValue;
    }
    updateAST();
}

return <>
    <Row>
      <Form.Label column>Value</Form.Label>
      <Col><Form.Control type="number" value={node.supplier && node.supplier()} 
            onChange={onChangeValue}/></Col>
    </Row>
</>;

}