import Selectable from "./Selectable";

function InnerNode(props) {
    let {children, className, selected, to_connect, setvalue, getvalue, ...other} = props;
    
    if (setvalue || getvalue){
        className += ' Wired ';
    }

    if (!children || children.length == 0)
        className += ' emptyNode ';

    if (to_connect)
        className += ' to_connect ';
    className += ' Node ';

    return (<div className={className} {...other}>
        {children}
    </div>);
}

const Node = Selectable(InnerNode);
export default Node;