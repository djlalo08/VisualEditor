package attempt2;

import static attempt2.At.at;

public class In_Binding<T> implements Input<T>{
	
	At<Output<T>> valueFrom;

	public In_Binding(At<Output<T>> from) {
		this.valueFrom = from;
	}
	
	@Override
	public T eval() {
		return valueFrom.obj.eval();
	}
	
	public static <T> At<Input<T>> from(At<Output<T>> from) {
		return at(new In_Binding<T>(from));
	}

}
