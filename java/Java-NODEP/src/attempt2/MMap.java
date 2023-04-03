package attempt2;

import static attempt2.Pair.pair;

import java.util.List;
import java.util.function.Function;

public class MMap<U, V> extends At<Pair<InList<U>, OutList<V>>> {

	public MMap(Pair<InList<U>, OutList<V>> obj) {
		super(obj);
		outs().parent = this;
	}

	public MMap(InList<U> ins, OutList<V> outs) {
		super(pair(ins, outs));
		outs().parent = this;
	}
	
	public MMap(String name, InList<U> ins, OutList<V> outs) {
		super(pair(ins, outs));
		outs().parent = this;
		addAttr("mapName", name);
	}
	
	public InList<U> ins() {
		return obj.a;
	}
	
	public OutList<V> outs() {
		return obj.b;
	}

	@SuppressWarnings("unchecked")
	public List<V> eval(){
		List<U> ins = ins().eval();
		
		List<? extends Object> ins_o = (List<Object>) ins;
		Function<List<? extends Object>, List<? extends Object>> map = MapsRepo.getMap(getAttr("mapName"));
		List<? extends Object> outs = map.apply(ins_o);
		
		return (List<V>) outs;
	}
	
}
