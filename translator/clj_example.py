clojure_code = '''
(defx
   min-max-avg
   [[:i0] [:i1 :ix]]
   [(make-map min-max [(outsmap :i0)] [:o0 :o1])
    (make-map div [(make-map add [(outsmap :o0) (outsmap :o1)] []) [2]] [:o2])]
   [[:o0] [:o2] [:o1]])
'''