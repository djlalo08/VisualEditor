import { addProps } from "../Utils/ReactUtils";

export function IfMap(props){
    let {id, className, ins, other} = props;
    let newIns = addProps(ins, {prefix:'t'}) ;
    return (<div id={id} className={className} {...other}>
        <span>

        <table style={
            {  display: 'block',
            'margin-left': 'auto',
            'margin-right': 'auto',
            width: '5%'}}>
            <tr>
                <td>
                    if
                </td>
                <td>
                {addProps(newIns, {onlyShowIdx:0, name:'if'})}
                </td>
            </tr>
        </table>
        <table>
            <tr>
                <td> then </td>
                <td> {addProps(newIns, {onlyShowIdx:1})} </td>
                <td style={{width: '12px'}}></td>
                <td style={{width: '1px', backgroundColor: 'gray'}}></td>
                <td style={{width: '25px'}}></td>
                <td> else </td>
                <td> {addProps(newIns, {onlyShowIdx:2})} </td>

            </tr>

        </table>
        </span>

    </div>)
}