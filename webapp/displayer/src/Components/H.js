export function H(props){
    let children = props.children;
    children = children.map(x => <td className="col_">{x}</td>) 
    return (<table><tbody>
        <tr>{children}</tr>
    </tbody></table>);
}