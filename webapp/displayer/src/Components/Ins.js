import { intersperse_i } from '../Utils/ListUtils';
import Grid from './Grid';
import Trtd from './Trtd';

export default function Ins(props){
    let {children, infix, prefix, postfix, name} = props

    if (!children || !children.length)
        return null;
    
    children = children.map((x, i) => <td key={i}>{x}</td>);
    if (infix)
        children = intersperse_i(children, i => <td key={name+i}>{name}</td>);
    else if (prefix)
        children.splice(0, 0, <td key={name}>{name}</td>);
    else if (postfix)
        children.push(<td key={name}>{name}</td>);

    return (<Trtd>
        <Grid>
            <tr>{children}</tr>
        </Grid>
    </Trtd>);
}