import Xarrow from "react-xarrows";

export default function Wire(props){
    return (
    <><Xarrow start={props.start} end={props.end}
        color="black"
        strokeWidth={2.4}
        headShape='circle'
        tailShape='circle'
        // path='grid'
        showHead={false}
        // showTail
        headSize={2.8}
        tailSize={2.8}
        startAnchor='bottom'
        endAnchor='top'
    />
    <Xarrow start={props.start} end={props.end}
        color="green"
        strokeWidth={2}
        headShape='circle'
        tailShape='circle'
        // path='grid'
        showHead={false}
        // showTail
        headSize={3}
        tailSize={3}
        startAnchor='bottom'
        endAnchor='top'
    /></>
    );
}