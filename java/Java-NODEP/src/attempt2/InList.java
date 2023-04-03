package attempt2;

import java.util.ArrayList;
import java.util.List;

public class InList<T> extends At<P<At<Input<T>>>>{

	public InList(P<At<Input<T>>> obj) {
		super(obj);
	}

	public List<At<Input<T>>> ins(){
		return obj;
	}
	
	public List<T> eval(){
		List<T> ins = new ArrayList<>();
		for (At<? extends Input<T>> input: ins()) {
			ins.add(input.obj.eval());
		}
		return ins;
	}

}
