package attempt2;

public class Constant<T> implements Input<T>{
	T value;
	
	public Constant(T value){
		this.value = value;
	}
	
	public static <T_> Constant<T_> of(T_ value){
		return new Constant<T_>(value); 
	}
	
	public T eval() {
		return value;
	}
}
