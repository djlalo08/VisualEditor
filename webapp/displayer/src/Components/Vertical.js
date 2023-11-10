export default function Vertical(props){
    let {children, invisible} = props;
    if (!children || !children.length)
        return null;

    if (invisible){
        return children;
    }

    let last_idx = children.length-1;
    children = children.map(
        (x,i) => 
        <tr key={i}><td className={i == last_idx? "": "row_"}>{x}</td></tr>);
    
    return (<table><tbody>
        {children}
    </tbody></table>);
}