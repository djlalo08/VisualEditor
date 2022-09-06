export default function Vertical(props){
    let childrens = props.children.map(
        (child, index) => <div key={index} style={{display: "block"}}>{child}</div>);

    return( <> {childrens} </>);
}