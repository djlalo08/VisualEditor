package attempt2;

import java.util.ArrayList;

public class P<T> extends ArrayList<T>{

	@SafeVarargs
	public static <T> P<T> of(T... items){
		P<T> p = new P<>();
		for (T item: items) {
			p.add(item);
		}
		return p;
	}
	
}
