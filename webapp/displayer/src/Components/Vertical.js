export default function Vertical(props){
    let children = props.children;
    if (!children || !children.length)
        return null;

    let last_idx = children.length-1;
    children = children.map(
        (x,i) => 
        <tr key={i}><td className={i == last_idx? "": "row_"}>{x}</td></tr>);
    
    return (<table><tbody>
        {children}
    </tbody></table>);
}