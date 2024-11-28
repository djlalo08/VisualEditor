export default function Grid(props){
    return (props.children 
        ?  <table><tbody>{props.children}</tbody></table>
        : null);
}