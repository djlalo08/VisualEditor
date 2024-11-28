import { intersperse_i } from '../Utils/ListUtils';
import { addProps } from '../Utils/ReactUtils';
import Grid from './Grid';
import Trtd from './Trtd';

export default function Ins(props){
    let {children, infix, prefix, postfix, name, onlyShowIdx, ...other} = props


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
    
    let propagateProps = child => child && addProps(child, {...other});
    children = children.length ? children.map(propagateProps) : propagateProps(children);

    return (<Trtd>
        <Grid>
            <tr>{children}</tr>
        </Grid>
    </Trtd>);
}