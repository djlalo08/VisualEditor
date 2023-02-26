import Selectable from "./Selectable";

function InnerNode(props) {
    let {children, className, selected, ...other} = props;

    return (<div className={props.className + " Node "} {...other}>
        {props.children}
    </div>);
}

const Node = Selectable(InnerNode);
export default Node;