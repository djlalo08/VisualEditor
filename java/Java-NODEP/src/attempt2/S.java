package attempt2;

import java.util.ArrayList;

public class S<T> extends ArrayList<T> {

	public static <T> S<T> empty(T t){
		return new S<T>();
	}
	
	public static <T> S<T> of(T... items){
		S<T> s = new S<>();
		for (T item: items) {
			s.add(item);
		}
		return s;
	}
	
}
