
import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 
public class Transpiler {
 public static void main(String[] args) throws IOException {
	Object[] result = quad(3.0,8.0,1.0);
File data_bus = new File("data_bus.txt");
data_bus.createNewFile();

FileWriter writer = new FileWriter("data_bus.txt");
for (Object o: result)
    writer.write(o + "\n");
writer.close();
}


public static Object[] div(Object... ins){
    Object[] result = new Object[1];
    result[0] = (double)ins[0]/(double)ins[1];
    return result;
}

public static Object[] mul(Object... ins){
    Object[] result = new Object[1];
    result[0] = (double)ins[0]*(double)ins[1];
    return result;
}

public static Object[] _$2(Object... in){
    Object[] result = new Object[1];
    result[0] = 2.0;
    return result;
}

public static Object[] plus(Object... ins){
    Object[] result = new Object[1];
    result[0] = (double)ins[0]+(double)ins[1];
    return result;
}

public static Object[] sqrt(Object... ins){
    Object[] result = new Object[1];
    result[0] = Math.sqrt((double)ins[0]);
    return result;
}

public static Object[] sub(Object... ins){
    Object[] result = new Object[1];
    result[0] = (double)ins[0]-(double)ins[1];
    return result;
}

public static Object[] mul3(Object... ins){
    Object[] result = new Object[1];
    result[0] = (double)ins[0]*(double)ins[1]*(double)ins[2];
    return result;
}

public static Object[] _$4(Object... in){
    Object[] result = new Object[1];
    result[0] = 4.0;
    return result;
}

public static Object[] square(Object... ins){
    Object[] result = new Object[1];
    result[0] = (double)ins[0]*(double)ins[0];
    return result;
}

public static Object[] det(Object... in){ Object[] out = new Object[1];
	Object[] square_10 = square(in[1]);
	Object[] _$4_20 = _$4();
	Object[] mul3_14 = mul3(_$4_20[0], in[0], in[2]);
	Object[] sub_5 = sub(square_10[0], mul3_14[0]);
	Object[] sqrt_1 = sqrt(sub_5[0]);
	out[0] = sqrt_1[0];
	return out;
}

public static Object[] neg(Object... ins){
    Object[] result = new Object[1];
    result[0] = -(double)ins[0];
    return result;
}


public static Object[] split2(Object... ins){
    Object[] result = new Object[2];
    result[0] = ins[0];
    result[1] = ins[0];
    return result;
}

public static Object[] quad(Object... in){ Object[] out = new Object[1];
	Object[] split2_16 = split2(in[1]);
	Object[] neg_44 = neg(split2_16[0]);
	Object[] split2_21 = split2(in[0]);
	Object[] det_26 = det(split2_21[1], split2_16[1], in[2]);
	Object[] plus_48 = plus(neg_44[0], det_26[0]);
	Object[] _$2_63 = _$2();
	Object[] mul_58 = mul(_$2_63[0], split2_21[0]);
	Object[] div_53 = div(plus_48[0], mul_58[0]);
	out[0] = div_53[0];
	return out;
}
}