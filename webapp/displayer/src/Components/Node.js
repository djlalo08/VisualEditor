export default function Node(props) {

    return (<div className={"Node " + props.className}>
        {props.children}
    </div>) 
}