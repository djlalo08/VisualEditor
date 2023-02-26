export default function Movable(InnerComponent){
    return (props =>  {
        let myProps = {...props};

        if (props.second_select) 
            myProps.className = " secondSelect " + props.className;
        return <InnerComponent {...myProps}/>;
    });

}