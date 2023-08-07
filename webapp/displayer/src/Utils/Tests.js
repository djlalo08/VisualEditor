import { openFile, setSelectedById } from "../Actions";

export function runTests(app){

    testLambdas(app);

}


async function testLambdas(app){
    await openFile('lambdas', () => setSelectedById(26, () => app.eval_([8,9,10,11,12])));
}