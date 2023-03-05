import { intersperse } from '../Utils/ListUtils';
import Grid from './Grid';
import Trtd from './Trtd';

export default function Outs(props){
    let {children, infix, name} = props

    if (!children || !children.length)
        return null;
    
    children = children && children.map((x, i) => <td key={i}>{x}</td>);
    if (infix)
        children = intersperse(children, <td>{name}</td>);

    return (<Trtd>
        <Grid>
            <tr>{children}</tr>
        </Grid>
    </Trtd>);
}