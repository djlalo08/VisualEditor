import Selectable from "./Selectable";

function InnerNode(props) {
    let {children, className, selected, to_connect, ...other} = props;
    
    if (to_connect)
        className += ' to_connect ';
    className += ' Node ';

    return (<div className={className} {...other}>
        {props.children}
    </div>);
}

const Node = Selectable(InnerNode);
export default Node;