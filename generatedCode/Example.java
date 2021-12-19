
public class Example{


    public static Object[] example(Object[] in){
        Object[] out = new Object[1];
        Object[] id_23 = id(in[1]); //b
        Object[] id_19 = id(in[0]); //a
        Object[] id_27 = id(in[2]); //c
        Object[] mul_62 = mul(id_23[0], id_23[0]); //b^2
        Object[] mul_37 = mul(id_19[0], id_27[0]); //a*b
        Object[] mul4_50 = mul4(mul_37[0]); //
        Object[] sub_75 = sub(mul_62[0], mul4_50[0]);
        Object[] sqrt_88 = sqrt(sub_75[0]);
        Object[] neg_58 = neg(id_23[0]);
        Object[] add_100 = add(sqrt_88[0], neg_58[0]);
        Object[] mul2_113 = mul2(id_19[0]);
        Object[] div_117 = div(add_100[0], mul2_113[0]);
        out[0] = div_117[0];
        return out;
    }


    public static Object[] add(Object...in){
        Object[] out = new Object[1];
        out[0] = (double)in[0] + (double)in[1];
        return out;
    }
    
    public static Object[] mul(Object...in){
        Object[] out = new Object[1];
        out[0] = (double)in[0] * (double)in[1];
        return out;
    }

    public static Object[] neg(Object...in){
        Object[] out = new Object[1];
        out[0] = -(double)in[0];
        return out;
    }

    public static Object[] sub(Object...in){
        Object[] out = new Object[1];
        out[0] = (double)in[0] - (double)in[1];
        return out;
    }

    public static Object[] div(Object...in){
        Object[] out = new Object[1];
        out[0] = (double)in[0] / (double)in[1];
        return out;
    }

    public static Object[] mul2(Object...in){
        Object[] out = new Object[1];
        out[0] = (double)in[0] * 2;
        return out;
    }

    public static Object[] mul4(Object...in){
        Object[] out = new Object[1];
        out[0] = (double)in[0] * 4;
        return out;
    }

    public static Object[] id(Object...in){
        Object[] out = new Object[1];
        out[0] = in[0];
        return out;
    }

    public static Object[] sqrt(Object...in){
        Object[] out = new Object[1];
        out[0] = Math.sqrt((double)in[0]);
        return out;
    }

    public static void main(String[] args) {
        Object[] in = new Object[3];
        in[0] = 12.0;
        in[1] = 30.0;
        in[2] = 17.0;
        Object[] out = example(in);
        for (Object o: out)
            System.out.println(o);
        
        double a = (double)in[0];
        double b = (double)in[1];
        double c = (double)in[2];
        double quadratic = (-b + Math.sqrt(b*b - 4*a*c))/(2*a);
        System.out.println(quadratic - (double)out[0]);
    }

}