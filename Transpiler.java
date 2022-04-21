
import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 
public class Transpiler {
 public static void main(String[] args) throws IOException {Object[] result = D_0E_0F_0A_0U_0L_0T();
    File data_bus = new File("data_bus.txt");
    data_bus.createNewFile();

    FileWriter writer = new FileWriter("data_bus.txt");
    for (Object o: result)
        writer.write(o + "\n");
    writer.close();
}


public static Object[] _$4(Object... in){
    Object[] result = new Object[1];
    result[0] = 4;
    return result;
}

public static Object[] D_0E_0F_0A_0U_0L_0T(Object... in){ Object[] out = new Object[1];
	Object[] _$4_1 = _$4();
	out[0] = _$4_1[0];
	return out;
}
}