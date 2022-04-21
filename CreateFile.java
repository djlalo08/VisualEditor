import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 

public class CreateFile {
  public static void main(String[] args) throws IOException {
    File data_bus = new File("data_bus.txt");
    data_bus.createNewFile();

    FileWriter writer = new FileWriter("data_bus.txt");
    writer.write("Files in Java might be tricky, but it is fun enough!");
    writer.close();
  }
}