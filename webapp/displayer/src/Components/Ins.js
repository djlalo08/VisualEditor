import { intersperse_i } from '../Utils/ListUtils';
import Grid from './Grid';
import Trtd from './Trtd';

export default function Ins(props){
    let {children, infix, prefix, postfix, name, onlyShowIdx} = props


    if (!children || !children.length)
        return null;
    
    children = children.map((x, i) => <td key={i}>{x}</td>);
    if (infix)
        children = intersperse_i(children, i => <td key={name+i}>{name}</td>);
    else if (prefix)
        children.splice(0, 0, <td key={name}>{name}</td>);
    else if (postfix)
        children.push(<td key={name}>{name}</td>);

    if (onlyShowIdx || onlyShowIdx===0){
        children = children[onlyShowIdx+1];
    }

    return (<Trtd>
        <Grid>
            <tr>{children}</tr>
        </Grid>
    </Trtd>);
}