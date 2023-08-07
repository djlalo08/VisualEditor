import { openFile, setSelectedById } from "../Actions";

export async function runTests(app){

    await assertList(app, 'lambdas', 11, [8,9,10,11,12]);
    await assertValue(app, 'lambdas', 4, 2);
    await assertValue(app, 'inc_test', 2, 6);

}

async function assertList(app, fileName, id, expectedList){
    let assertFn = actualValue => {
        if (expectedList.every((val, idx) => actualValue[idx] == val)){
            console.log(`Correct value of id ${id} at ${fileName}`);
        } else {
            console.log(`Wrong value at '${fileName}'! Expected ${expectedList} at id ${id} but got:`);
            console.log(actualValue);
        }
    }
    await runTest(app, fileName, id, assertFn);    
}

async function assertValue(app, fileName, id, expectedValue){
    let assertFn = actualValue => {
        if (actualValue == expectedValue){
            console.log(`Correct value of id ${id} at ${fileName}`);
        } else {
            console.log(`Wrong value at '${fileName}'! Expected ${expectedValue} at id ${id} but got:`);
            console.log(actualValue);
        }
    }
    await runTest(app, fileName, id, assertFn);
}

async function runTest(app, fileName, id, assertFn){
    await openFile(fileName, () => setSelectedById(id, () => app.eval_(assertFn)));
}