import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class Example{

    public static List<Object> addUser(int addUserIn1, int addUserIn2){
        List<Object> add_result_1 = add(addUserIn1, addUserIn2);
        int add_result_1_var_1 = (int) add_result_1.get(0);
        List<Object> returns = new LinkedList<>();
        returns.add(add_result_1_var_1);
        return returns;
    }

    public static List<Object> add(int a, int b){
        return Arrays.asList(a + b);
    }
    
    public static void main(String[] args) {
        List<Object> result = addUser(23, 46);
        int value = (int) result.get(0);
        System.out.println(value);
    }

}