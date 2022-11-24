import Selectable from "./Selectable";

function InnerNode(props) {

    return (<div className={"Node " + props.className}>
        {props.children}
    </div>) 
}

const Node = Selectable(InnerNode);
export default Node;