import React from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import { getNameAndAttrs } from '../Utils/NodeUtils';
import { MapSidebar } from './MapSidebar';

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
    let props = {attrs, node};
    switch(name){
        case 'Map':
            return <MapSidebar {...props}/>;
    }
}
