import { app } from '../Actions';
import { ast_to_jsx } from '../Utils/Converter';
import { parse } from '../Utils/IrToAst';
import { printAst } from '../Utils/NodeUtils';

const UNDO_LIMIT = 5;
//TODO when lastIRs list goes over UNDO_LIMIT keep only the last UNDO_LIMIT

export function save_snapshot() {
    app.state.lastIRs.push(printAst(app.state.AST));
    app.setState({ lastIRs: [...app.state.lastIRs], nextIRs: [] });
}

export function undo() {
    if (!app.state.lastIRs.length)
        return;
    app.state.nextIRs.push(printAst(app.state.AST));

    let AST = parse(app.state.lastIRs.pop());
    let [JSX, selected] = ast_to_jsx(AST);
    app.setState({ AST, JSX, selected, lastIRs: [...app.state.lastIRs], nextIRs: [...app.state.nextIRs] });
}

export function redo() {
    if (!app.state.nextIRs.length)
        return;
    app.state.lastIRs.push(printAst(app.state.AST));

    let AST = parse(app.state.nextIRs.pop());
    let [JSX, selected] = ast_to_jsx(AST);
    app.setState({ AST, JSX, selected, lastIRs: [...app.state.lastIRs], nextIRs: [...app.state.nextIRs] });
}
