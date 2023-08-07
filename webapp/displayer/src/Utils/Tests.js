import { openFile, setSelectedById } from "../Actions";

export async function runTests(app){

    await runTest(app, 'lambdas', 11, [8,9,10,11,12]);
    // await runTest(app, 'lambdas', 4, 2);


}

async function runTest(app, fileName, id, expectedVal){
    await openFile(fileName, () => setSelectedById(id, () => app.eval_(expectedVal)));
}