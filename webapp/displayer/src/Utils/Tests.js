import { openFile, setSelectedById } from "../Actions";

export async function runTests(app){

    await assertList(app, 'lambdas', 11, [8,9,10,11,12]);
    await assertValue(app, 'lambdas', 4, 2);
    await assertValue(app, 'inc_test', 2, 6);
    await assertNestedList(app, 'lambda_nest', 28, [[3,4,5], [3,4,5], [3,4,5]]);

}

async function assertNestedList(app, fileName, id, expectedList){
    let assertFn = actualValue => {
        if (expectedList.every(
                (ls, i) => ls.every( 
                    (val, j) => 
                        val == actualValue[i][j]
                ))
        ){
            console.log(`Correct value of id ${id} at ${fileName}`);
        } else {
            console.log(`Wrong value at '${fileName}'! Expected ${expectedList} at id ${id} but got:`);
            console.log(actualValue);
        }
    }
    await runTest(app, fileName, id, assertFn);  
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
    openFile(fileName);
    await sleep(100);
    setSelectedById(id);
    await sleep(1);
    app.eval_(assertFn);
}

function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}