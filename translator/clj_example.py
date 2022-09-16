clojure_code = '''
(defx
  min-max-avg
  [(m {"name" "ls"} [:ix]) [:i1 :i0]]
  [(make-map min-max [(outsmap :i0)] [:o0 :o1])
   (m {"infix" "true"} (make-map / [(m {"infix" "true"} (make-map + [(outsmap :o0) (outsmap :o1)] [])) (m {"className" "constant"} [2])] [:o2]))]
  [(m {"name" "min"} [:o0]) (m {"name" "avg"} [:o2, :o1]) (m {"name" "max"} [:o1])])
  '''