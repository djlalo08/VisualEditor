import { app } from '../Actions';
import { parse } from '../Utils/IrToAst';
import { getImports, printAst } from '../Utils/NodeUtils';


export async function openFile(fileName) {
    let response = await fetch(`./irs/${fileName}.ir`);
    let text = await response.text();
    app.setState(app.stateFromIR(text), () => loadImports(app.state.AST));
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

        fetch(`${location}${name}.ir`)
            .then(response => response.text())
            .then(importCode => {
                let import_irs = {};
                for (let [name, ast] of Object.entries(app.state.import_irs)) {
                    import_irs[name] = ast;
                }
                let ast = parse(importCode);
                import_irs[name] = ast;
                loadImports(ast);
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
