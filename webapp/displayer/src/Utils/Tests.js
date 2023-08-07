import { openFile, setSelectedById } from "../Actions";

export function runTests(app){

    // runTest(app, 'lambdas', 26, [8,9,10,11,12]);
    runTest(app, 'lambdas', 7, 2);


}

async function runTest(app, fileName, id, expectedVal){
    await openFile(fileName, () => setSelectedById(id, () => app.eval_(expectedVal)));
}