import { callEval, openFile, setSelectedById } from "../Actions";

let successful_tests = 0;
let total_tests = 0;

export async function runTests(app){

    await assertValue(app, 'inc_test', 2, 6);
    await assertNestedList(app, 'lambda_nest', 28, [[3,4,5], [3,4,5], [3,4,5]]);
    await assertList(app, 'lambdas', 11, [8,9,10,11,12]);
    await assertValue(app, 'lambdas', 4, 2);
    await assertValue(app, 'if_test', 2, 'ByeWorld');
    await assertValue(app, 'if_test', 14, 'HelloWorld');
    await assertList(app, '2_arg_lambda', 27, [10,12]);
    await assertValue(app, '!_runner', 6, 40320);
    await assertValue(app, 'import_chain_test', 6, 15);
    await assertValue(app, 'simple', 27, 3);
    await assertValue(app, 'simple', 28, -3);
    await assertList(app, 'filter_test', 11, [4,2]);
    await assertValue(app, 'variable_test', 14, 7);
    await assertValue(app, 'variable_test', 20, 10);
    await assertValue(app, 'vertical_test', 28, 9);    
    await assertList(app, 'quicksort_test', 2, [2,4,5,6,8]);
    await assertValue(app, 'x', 2, 12);

    console.log(`Testing completed. ${successful_tests}/${total_tests} tests successful`);
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
            successful_tests++;
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
            successful_tests++;
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
            successful_tests++;
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
    callEval(assertFn);
    await sleep(1);
    total_tests++;
}

function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}