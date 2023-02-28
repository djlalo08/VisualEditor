export function V(props){
    let children = props.children;
    children = children.map( x => <tr className="row_"><td>{x}</td></tr>);
    
    return (<table><tbody>
        {children}
    </tbody></table>);
}