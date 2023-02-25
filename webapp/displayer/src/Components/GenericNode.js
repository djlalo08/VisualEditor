import React from "react";

export default class GenericNode extends React.Component {
    constructor(props){
        super(props);
    }
    
    render(){
        let {nodeName, children} = this.props;
        return(<div className={nodeName}>
            {nodeName}
            {children}
        </div>);
    }
}