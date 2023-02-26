export default function Movable(InnerComponent){
    return (props =>  {
        let myProps = {...props};

        if (props.to_move) 
            myProps.className = " toMove " + props.className;
        return <InnerComponent {...myProps}/>;
    });

}