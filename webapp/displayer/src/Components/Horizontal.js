export default function Horizontal(props){
    let children = props.children;
    if (!children || !children.length)
        return null;

    children = children.map((x,i) => <td key={i} className="col_">{x}</td>) 

    return (<table><tbody>
        <tr>{children}</tr>
    </tbody></table>);
}