package attempt2;

import static attempt2.At.at;
import static attempt2.In_Binding.from;

public class Runner {

	public static void main(String [] args) {
		
		At<Input<Double>> A = at(Constant.of(5.));
		At<Input<Double>> B = at(Constant.of(30.));
		At<Input<Double>> C = at(Constant.of(8.));
 		At<Input<Double>> FOUR = at(Constant.of(4.));

 		
 		InList<Double> il1 = new InList<Double>(P.of(FOUR, A, C));
 		
 			At<Output<Double>> o1 = at(new Out_Binding<Double>());
 		OutList<Double> ol1 = new OutList<Double>(P.of(o1));
		
 		MMap<Double, Double> mul = new MMap<>("mul", il1, ol1);

 		System.out.println(o1.obj.eval());
 		
 		
 		InList<Double> il2 = new InList<Double>(P.of(B));
 			At<Output<Double>> o2 = at(new Out_Binding<>());
 		OutList<Double> ol2 = new OutList<Double>(P.of(o2));
 		MMap<Double, Double> sqr = new MMap<>("sqr", il2, ol2);
 		
 		System.out.println(o2.obj.eval());
 		
 		
 		InList<Double> il3 = new InList<Double>(P.of(from(o2), from(o1)));
 			At<Output<Double>> o3 = at(new Out_Binding<Double>());
 		OutList<Double> ol3 = new OutList<Double>(P.of(o3));
 		
 		MMap<Double, Double> sub = new MMap<>("sub", il3, ol3);
 		
 		System.out.println(o3.obj.eval());
 		
		InList<Double> il4 = new InList<>(P.of(from(o3)));
			At<Output<Double>> o4 = at(new Out_Binding<Double>());
		OutList<Double> ol4 = new OutList<Double>(P.of(o4));
				
		MMap<Double, Double> sqrt = new MMap<>("sqrt", il4, ol4);
		
		System.out.println(o4.obj.eval());
		
		
		Node root = new Node(S.of(mul, sqr, sub));
		
		
	}
	
}








