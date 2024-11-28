import { app } from '../Actions';
import { parse } from '../Utils/IrToAst';
import { getFunctions, getImports, printAst } from '../Utils/NodeUtils';


export async function openFile(fileName) {
    let openTheFile = async function(){
        let response = await fetch(`./irs/${fileName}.ir`);
        let text = await response.text();
        app.setState(app.stateFromIR(text), () => loadImports(app.state.AST));
    }
    app.setState({activeFile: fileName}, openTheFile);
}

export async function openFileFromModal() {
    await openFile(app.state.modalText);
    app.setState({ activeFile: app.state.modalText });
}

export async function openFileFromDir() {
    app.setState({ modalAction: openFileFromModal, modalText: '', showModal: true });
}
function loadImports(node) {
    let imports = getImports(node);
    for (let [name, location] of Object.entries(imports)) {
        if (app.state.import_irs[name])
            continue;

        fetch(`${location}.ir`)
            .then(response => response.text())
            .then(importCode => {
                let import_irs = {};
                for (let [name, ast] of Object.entries(app.state.import_irs)) {
                    import_irs[name] = ast;
                }
                let ast = parse(importCode);
                let functions = getFunctions(ast);
                if (functions[name]){
                    import_irs[name] = functions[name];
                    loadImports(functions[name]);
                }
                app.setState({ import_irs });
            });
    }
}
export async function save() {
    console.log(`${app.state.activeFile} saved!`);
    let fileHandle = await app.state.irDirHandle.getFileHandle(`${app.state.activeFile}.ir`);
    let writable = await fileHandle.createWritable();
    await writable.write(printAst(app.state.AST));
    await writable.close();
}
