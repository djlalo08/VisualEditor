import { addProps } from "../Utils/ReactUtils";

export function IfMap(props){
    let {id, className, ins, other} = props;
    let newIns = addProps(ins, {prefix:'t'}) ;
    let divider = (<>
        <td style={{width: '8px'}}></td>
        <td style={{width: '1px', backgroundColor: 'lightgray'}}></td>
        <td style={{width: '1px'}}></td>
        <td style={{width: '1px', backgroundColor: 'dimgray'}}></td>
        <td style={{width: '1px'}}></td>
        <td style={{width: '1px', backgroundColor: 'lightgray'}}></td>
        <td style={{width: '8px'}}></td>
    </>
    );

    return (<div id={id} style={{textAlign: 'center'}} className={className} {...other}>
        <span>
        <table style={{display: 'inline-block'}}>
            <tr>
                <td>if</td>
                <td>{addProps(newIns, {onlyShowIdx:0, name:'if'})}</td>
            </tr>
        </table>
        <table>
            <tr>
                <td> then </td>
                {divider}
                <td> else </td>
            </tr>
            <tr>
                <td> {addProps(newIns, {onlyShowIdx:1})} </td>
                {divider}
                <td> {addProps(newIns, {onlyShowIdx:2})} </td>
            </tr>
        </table>
        </span>
    </div>)
}