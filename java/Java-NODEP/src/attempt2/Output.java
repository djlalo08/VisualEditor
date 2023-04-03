package attempt2;

public interface Output<T> {

	public T eval();
	
	public void setParent(OutList<T> parent);
	
	public void setIndex(int index);
	
	public String toString();
}
