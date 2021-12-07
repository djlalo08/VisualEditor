
public class Example{

    public static Object[] example(Object[] in){
        Object[] out = new Object[2];
        Object[] fn_1 = add(in[0], in[1]);
        out[0] = fn_1[0];
        out[1] = fn_1[1];
        return out;
    }

    public static Object[] add(Object...in){
        Object[] out = new Object[1];
        out[0] = (int)in[0] + (int)in[1];
        return out;
    }
    
    public static Object[] mul(Object...in){
        Object[] out = new Object[1];
        out[0] = (int)in[0] * (int)in[1];
        return out;
    }

    public static Object[] neg(Object...in){
        Object[] out = new Object[1];
        out[0] = -(int)in[0];
        return out;
    }

    public static Object[] sub(Object...in){
        Object[] out = new Object[1];
        out[0] = (int)in[0] - (int)in[0];
        return out;
    }

    public static Object[] div(Object...in){
        Object[] out = new Object[1];
        out[0] = (int)in[0] / (int)in[0];
        return out;
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