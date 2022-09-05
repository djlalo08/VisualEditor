import Xarrow from "react-xarrows";

export default function Wire(props){
    return (<Xarrow start={props.start} end={props.end}
        color="green"
        strokeWidth={2}
        headShape='circle'
        // path='grid'
        showHead={false}
    />);
}