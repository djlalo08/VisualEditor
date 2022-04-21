
import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 
public class Transpiler {
 public static void main(String[] args) throws IOException {Object[] result = ref_test(12350,1234);
    File data_bus = new File("data_bus.txt");
    data_bus.createNewFile();

    FileWriter writer = new FileWriter("data_bus.txt");
    for (Object o: result)
        writer.write(o + "\n");
    writer.close();
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
	Object[] sub_test_16 = sub_test(in[0], in[1]);
	out[0] = sub_test_16[0];
	return out;
}
}