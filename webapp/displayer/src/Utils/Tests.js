import { callEval } from "../Actions";
import { openFile } from '../Actions/FileActions';
import { setSelectedById } from '../Actions/SelectionActions';

let successful_tests = 0;
let total_tests = 0;

export async function runTests(app){

    await assertValue(app, 'inc_test', 12, 6);
    await assertNestedList(app, 'lambda_nest', 56, [[3,4,5], [6,7,8], [9,10,11]]);
    await assertNestedList(app, 'lambda_nest', 76, [[41,42,43], [44,45,46], [47,48,49]]);
    await assertList(app, 'lambdas', 26, [8,9,10,11,12]);
    await assertValue(app, 'lambdas', 4, 2);
    await assertValue(app, 'if_test', 2, 'ByeWorld');
    await assertValue(app, 'if_test', 26, 'HelloWorld');
    await assertList(app, '2_arg_lambda', 40, [10,12]);
    await assertValue(app, '!', 9, 40320);
    await assertValue(app, 'import_chain_test', 9, 15);
    await assertValue(app, 'simple', 39, 3);
    await assertValue(app, 'simple', 40, -3);
    await assertList(app, 'filter_test', 26, [4,2]);
    await assertValue(app, 'variable_test', 23, 7);
    await assertValue(app, 'variable_test', 32, 10);
    await assertValue(app, 'vertical_test', 49, 9);    
    await assertList(app, 'quicksort', 1, [2,4,5,6,8]);
    await assertValue(app, 'fib', 9, 89);
    await assertList(app, '2_outs_test', 1, [8,2]);

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
    await sleep(300);
    setSelectedById(id);
    await sleep(10);
    callEval(assertFn);
    await sleep(10);
    total_tests++;
}

function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}