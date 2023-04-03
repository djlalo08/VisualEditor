package attempt2;

import java.util.List;

public class OutList<T> extends At<P<At<Output<T>>>>{

	MMap<? extends Object, T> parent;
	
	public OutList(P<At<Output<T>>> obj) {
		super(obj);
		for (int i = 0; i < obj.size(); i++) {
			obj.get(i).obj.setParent(this);
			obj.get(i).obj.setIndex(i);
		}
		String n = obj.get(0).getAttr("name");
	}
	
	public List<T> eval(){
		return parent.eval();
	}

}
