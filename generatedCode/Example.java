
public class Example{

    public static Object[] example(Object[] in){
        //Generated code for: (-b + b^2-ac)/a
        Object[] out = new Object[1];
        Object[] id_29 = id(in[0]); // a
        Object[] id_25 = id(in[1]); // b 
        Object[] id_33 = id(in[2]); // c
        Object[] mul_56 = mul(id_25[0], id_25[0]); // b^2
        Object[] mul_43 = mul(id_29[0], id_33[0]); // a*c
        Object[] sub_86 = sub(mul_56[0], mul_43[0]); // b^2 - a*c
        Object[] neg_69 = neg(id_25[0]); // -b
        Object[] add_99 = add(sub_86[0], neg_69[0]); // -b + b^2 - a*c
        Object[] div_112 = div(add_99[0], id_29[0]); // (-b + b^2 - a*c)/a
        out[0] = div_112[0];
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
        out[0] = (int)in[0] - (int)in[1];
        return out;
    }

    public static Object[] div(Object...in){
        Object[] out = new Object[1];
        out[0] = (int)in[0] / (int)in[1];
        return out;
    }

    public static Object[] id(Object...in){
        Object[] out = new Object[1];
        out[0] = in[0];
        return out;
    }

    public static void main(String[] args) {
        Object[] in = new Object[3];
        in[0] = 12;
        in[1] = 4;
        in[2] = 17;
        Object[] out = example(in);
        for (Object o: out)
            System.out.println(o);
    }

}