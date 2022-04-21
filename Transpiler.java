import java.util.Arrays;

public class Transpiler {
public static void main(String[] args) {
	 System.out.println("hi");
}

public static Object[] sub(Object... ins){
    Object[] result = new Object[1];
    result[0] = (int)ins[0]-(int)ins[1];
    return result;
}

public static Object[] sub_test(Object... in){
    Object[] out = new Object[1];
	Object[] sub_1 = sub(in[0], in[1]);
	out[0] = sub_1[0];
	return out;
}

public static Object[] ref_test(Object... in){
    Object[] out = new Object[1];
	Object[] sub_test_1 = sub_test(in[0], in[1]);
	out[0] = sub_test_1[0];
	return out;
}
}