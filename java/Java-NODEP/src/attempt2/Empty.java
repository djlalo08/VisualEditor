package attempt2;

public class Empty implements Input<Empty>, Output<Empty>{

	@Override
	public Empty eval() {
		throw new RuntimeException("Tried to evaluate an empty");
	}

	@Override
	public void setParent(OutList parent) {
	}

	@Override
	public void setIndex(int index) {
	}

}
