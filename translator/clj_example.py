clojure_code = \
    '''(defn min-max-avg [ls]
           (do-vertical
           (make-map min-max ls [:o0 :o1])
           (make-map / [(make-map + [(outsmap :o0) (outsmap :o1)] []) 2] [:o2])
           (vector (outsmap :o0) (outsmap :o1) (outsmap :o2))))'''
