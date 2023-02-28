import { intersperse } from "./Utils/ListUtils";

export function Mapx(props){
    let [ins, outs] = props.children;
    ins = ins.map(x => <td>{x}</td>);
    outs = outs.map(x => <td>{x}</td>);
    
    if (props.infix)
        ins = intersperse(ins, <td>{props.name}</td>);
    
    let in_comp = (<tr>
        <td>
            <table><tbody>
                <tr>{ins}</tr>     
            </tbody></table>
        </td>
    </tr>);
    
    let out_comp = ( <tr>
        <td>
            <table><tbody>
                <tr>{outs}</tr>     
            </tbody></table>
        </td>
    </tr>
    )


    return (<table className="Map"><tbody>
        {ins.length? in_comp: null}

        {props.infix? null: <tr><td>{props.name}</td></tr>}
        
        {outs.length? out_comp: null}
    </tbody></table>);
}