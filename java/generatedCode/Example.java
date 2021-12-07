import java.util.Arrays;
import java.util.List;

public class Example{

    public static Object[] example(Object[] in){
        Object[] out = new Object[2];
        Object[] fn_1 = fn(in[0], in[1]);
        out[0] = fn_1[0];
        out[1] = fn_1[1];
        return out;
    }

    public static Object[] fn(Object...in){
        Object[] out = new Object[2];
        out[0] = in[0];
        out[1] = (int)in[0] + (int)in[1];
        return out;
    }

    public static List<Object> add(int a, int b){
        return Arrays.asList(a + b);
    }
    
    public static void main(String[] args) {
        Object[] in = new Object[2];
        in[0] = 20;
        in[1] = 20;
        Object[] out = example(in);
        for (Object o: out)
            System.out.println(o);
    }

}