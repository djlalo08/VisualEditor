import React from "react";

export function addProps(component, props){
    return React.cloneElement(component, props);
}