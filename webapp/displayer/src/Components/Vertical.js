export default function Vertical(props){
    
    let childrens = props.children;
    childrens = Array.isArray(childrens) ? childrens : [childrens];
    childrens = childrens.map(
        (child, index) => <div key={index} style={{display: "block"}}>{child}</div>);

    return( <> {childrens} </>);
}