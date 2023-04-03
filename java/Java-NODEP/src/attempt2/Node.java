package attempt2;

public class Node extends At<S<MMap>> implements Input{

	public Node(S<MMap> obj) {
		super(obj);
	}

	@Override
	public Object eval() {
		return null; //TODO this is something like find all "active" output bindings in S, evaluate each, and return as list
	}

}
