clojure_code = '''
(defx 
  quadratic
  [[:a] [:b] [:c]]
  [(make-map sqrt [(m {"infix" "true"} (make-map - [(make-map sqr [(outsmap :b)] [])
                                                    (m {"infix" "true"} (make-map * [(m {"className" "constant"} [4]) (outsmap :a) (outsmap :c)] []))]
                                                 []))]
             [:discr])]
  [[:discr]])
  '''