export default function Selectable(InnerComponent){
    return (props =>  {
        let myProps = {...props};
        if (props.selected) 
            myProps.className = "selected " + props.className;
        return InnerComponent(myProps);
    })
}