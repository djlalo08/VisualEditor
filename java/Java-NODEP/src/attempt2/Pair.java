package attempt2;

public class Pair<A,B> {

	A a;
	B b;
	
	private Pair(A a, B b) {
		this.a = a;
		this.b = b;
	}
	
	public static <A, B> Pair<A,B> pair(A a, B b) {
		return new Pair<A, B>(a, b);
	}
}
