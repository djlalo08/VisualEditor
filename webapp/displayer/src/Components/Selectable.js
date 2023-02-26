import { updateSelected } from "../Actions";

export default function Selectable(InnerComponent){
    return (props =>  {
        let myProps = {...props};

        let on_click = (e) => {
            e.stopPropagation();
            updateSelected(myProps.ast_node);
        }

        if (props.selected) 
            myProps.className = " selected " + props.className;
        return <InnerComponent onClick={on_click} {...myProps}/>;
    });

}