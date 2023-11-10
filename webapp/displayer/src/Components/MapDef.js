import Node from "./Node";

export function MapDef(props){
    let {id, className, selected, children, other, name} = props;
    let [ins, outs, body] = children;
    let nameStyle = {padding: '0px 2px', margin: '1px'};
    if (selected){
        nameStyle.borderStyle = 'dashed';
        nameStyle.borderColor = 'rgb(184, 88, 88)';
        nameStyle.borderLeft = 'none';
        nameStyle.borderRight = 'none';
    }

    return (<div style={{'textAlign': 'left'}}>
        <span style={{display: 'flex', justifyContent: 'space-between', alignItems:'center'}}>
        {ins}
        <div style={nameStyle}>{name}</div>
        </span>
            <Node style={{borderStyle: 'inset'}}>
            {body}
            </Node>
        <div style={{display:'flex', justifyContent:'flex-end'}}>
            {outs}
        </div>
        <br/>
        <br/>
    </div>);
}