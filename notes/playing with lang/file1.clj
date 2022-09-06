(defmacro do-horizontal [& stmts]
  `(do ~@stmts))

(defmacro do-vertical [& stmts]
  `(do ~@stmts))

(def outsmap {})

(defn output [name value]
  (def outsmap (assoc outsmap name value)))

(defn make-map [map-name [& inputs] [& outputs]] 
  (let [results (apply map-name inputs)] 
    (doseq [[a b] (map vector outputs results)]
      (output a b)
     ((vector [results]) 0))))

(defn min-max [ls]
  (vector (apply min ls) (apply max ls)))

(defn min-max-avg [ls]
  (do-vertical
   (make-map min-max ls [:o0 :o1])
   (make-map / [(make-map + [(outsmap :o0) (outsmap :o1)] []) 2] [:o2])
   (vector (outsmap :o0) (outsmap :o1) (outsmap :o2))))

(defn div [[& as] [& bs]]
  (for [a as b bs] (/ a b)))

(defn add [& as] 
  (vector (apply + as)))


;; (min-max-avg [1,2,3,4,5])
(defn x []
  (do-vertical
   (make-map min-max [[1,2,3,4,5]] [:o0 :o1])
   ((make-map div [
                   [(make-map add [(outsmap :o0) (outsmap :o1)] [])]
                   [2]]
                  [:o2]))
   (vector (outsmap :o0) (outsmap :o1) (outsmap :o2))))

(defn read-inputs [input-names input-values]
  (let [r (map vector input-names input-values)]
    (doseq [[a b] r]
      (output a b))))

;; (read-inputs [:i0 :i1 :i2] [[1,2,3] 8 "hi"])

(defmacro defx [[ins in-vals] lines outs] 
  (list 'do
     (list 'read-inputs ins in-vals)
     (list 'doseq ['line lines] (list 'list 'line))
     (list 'map 'outsmap outs))) 

(println "c " outsmap)

(defx
  [[:i0 :i1] [[1,2,3,4,5] "hi"]]
  [(make-map min-max [(outsmap :i0)] [:o0 :o1])]
  [:o0 :o1])

(println "mcrexp "
 (macroexpand
  '(defx
     [[:i0] [[1,2,3]]]
     [(output :iii 3)]
     [:iii])))

;; (def result (defx [[:i0, :i1] [[1,2,3], "hi"]] [:i1] [(output :iii 3)]))

;; (println "result " result)
(println "d " outsmap)