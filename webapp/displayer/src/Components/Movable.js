export default function Movable(InnerComponent){
    return (props =>  {
        let myProps = {...props};

        if (props.toMove) 
            myProps.className = " toMove " + props.className;
        return <InnerComponent {...myProps}/>;
    });

}