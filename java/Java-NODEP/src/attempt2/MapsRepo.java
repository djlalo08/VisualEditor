package attempt2;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

public class MapsRepo {
	
	public static Map<String, Function<List<? extends Object>, List<? extends Object>>> maps;
	static {
	    maps = new HashMap<>();
	    maps.put("add", MapsRepo::add);
	    maps.put("mul", MapsRepo::mul);
	    maps.put("sqr", MapsRepo::sqr);
	    maps.put("sub", MapsRepo::sub);
	    maps.put("sqrt", MapsRepo::sqrt);

	}
	
	public static Function<List<? extends Object>, List<? extends Object>> getMap(String name){
		return (Function<List<? extends Object>, List<? extends Object>>) maps.get(name);
	}
	
	@SuppressWarnings("unchecked")
	public static List<Object> add(List<? extends Object> ins){
		List<Double> ins_i = (List<Double>) ins;

		double s = 0;
		for (Double i: ins_i) {
			s+= i;
		}
		return Arrays.asList(s);
	}
	
	@SuppressWarnings("unchecked")
	public static List<Object> mul(List<? extends Object> ins){
		List<Double> ins_i = (List<Double>) ins;

		double s = 1;
		for (Double i: ins_i) {
			s*= i;
		}
		return Arrays.asList(s);
	}

	@SuppressWarnings("unchecked")
	public static List<Object> sqr(List<? extends Object> ins){
		List<Double> ins_i = (List<Double>) ins;
		List<Object> outs_d = new ArrayList<>();
		
		for (Double i: ins_i) {
			outs_d.add(i*i);
		}
		return outs_d;
	}
	
	@SuppressWarnings("unchecked")
	public static List<Object> sub(List<? extends Object> ins){
		List<Double> ins_i = (List<Double>) ins;
		
		double s = ins_i.get(0)*2;
		for (Double i: ins_i) {
			s -= i;
		}
		return Arrays.asList(s);
	}

	@SuppressWarnings("unchecked")
 	public static List<Object> sqrt(List<? extends Object> ins){
		List<Double> ins_i = (List<Double>) ins;
		List<Object> outs_d = new ArrayList<>();
		
		for (Double i: ins_i) {
			outs_d.add(Math.sqrt(i));
		}
		return outs_d;
	}

	
}
