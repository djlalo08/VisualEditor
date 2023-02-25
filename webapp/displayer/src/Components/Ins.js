import { intersperse } from '../Utils/ListUtils';

export default function Ins(props){
    let {children, infix, name} = props
    return infix? intersperse(children, name) : children;
}