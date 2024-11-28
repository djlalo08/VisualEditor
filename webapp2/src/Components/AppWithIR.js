
export default class AppWithIR extends React.Component {

    constructor(props){
        super(props);
        this.state = {ir: null};
    }
    
    render(){
        let {ir} = this.state;
        return ir_to_components(ir);
    }
}