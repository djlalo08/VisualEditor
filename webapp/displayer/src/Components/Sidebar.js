import React from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import { getNameAndAttrs } from '../Utils/NodeUtils';
import { ConstantSidebar } from './Sidebars/ConstantSidebar';
import { InBoundSidebar } from './Sidebars/InBoundSidebar';
import { MapSidebar } from './Sidebars/MapSidebar';

export function Sidebar({node, AST}) {
    if (!node)
        return;

    let [name, attrs]  = getNameAndAttrs(node);
    
    return (
        <Offcanvas show={true} scroll={true} backdrop={false} placement='end'>
            <Offcanvas.Header>
                <Offcanvas.Title>{name}: {attrs.name}</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
                {body(name, attrs, node, AST)}
            </Offcanvas.Body>
        </Offcanvas>
    );
}

function body(name, attrs, node, AST){
    let props = {attrs, node, AST};
    if (attrs.value)
        return <ConstantSidebar {...props}/>;
        
    if (attrs.bind_idx || attrs.supplier)
        return <InBoundSidebar {...props}/>;

    switch(name){
        case 'Map':         return <MapSidebar {...props}/>;
        case 'InBound':     return <InBoundSidebar {...props}/>;
    }
}
