export default function Node(props) {

    return (<div id={props.id} className="Node">
        {props.children}
    </div>) 
}