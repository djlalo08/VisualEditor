package attempt2;

import java.util.HashMap;
import java.util.Map;

public class At<T> {
	
	Map<String, String> attrs = new HashMap<>();
	T obj;
	
	public At(T obj){
		this.obj = obj;
	}
	
	public static <T> At<T> at(T obj){
		return new At<T>(obj);
	}
	
	public void addAttr(String attrName, String value) {
		attrs.put(attrName, value);
	}
	
	public String getAttr(String attrName) {
		return attrs.get(attrName);
	}
	
}
