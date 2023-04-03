package attempt2;

public class Out_Binding<T> implements Output<T> {

	OutList<T> parent;
	int index;
	
	public T eval() {
		return parent.eval().get(index);
	}

	@Override
	public void setParent(OutList<T> parent) {
		this.parent = parent;
	}

	@Override
	public void setIndex(int index) {
		this.index = index;
	}
	
	
	public String toString() {
		return parent.toString()+ " : " + index;
	}
}
