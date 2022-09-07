(defmacro do-horizontal [& stmts]
  `(do ~@stmts))

(defmacro do-vertical [& stmts]
  `(do ~@stmts))

(def outsmap {})

(defn output [name value]
  (def outsmap (assoc outsmap name value)))

(defn make-map [map-name inputs outputs]
  (let [results (apply map-name inputs)]
    (doseq [[a b] (map vector outputs results)]
      (output a b))
    (identity results)))

(defn min-max [ls]
  (vector (apply min ls) (apply max ls)))

(defn div [as bs]
  (for [a as b bs] (/ a b)))

(println (div [10 20 30] [1 2 6]))

(defn add [& as]
  (vector (apply + as)))

(defn read-inputs [input-names input-values]
  (let [r (map vector input-names input-values)]
    (doseq [[a b] r]
      (output a b))))

;; (read-inputs [:i0 :i1 :i2] [[1,2,3] 8 "hi"])

(defmacro defx [name ins lines outs]
  (list 'def name
        (list 'fn
              '[& in-vals]
              (list 'do
                    (list 'read-inputs ins 'in-vals)
                    (list 'doseq ['line lines] (list 'list 'line))
                    (list 'map 'outsmap outs)))))

(println "c " outsmap)

(println
 (defx
   min-max-avg
   [:i0 :i1]
   [(make-map min-max [(outsmap :i0)] [:o0 :o1])
    (make-map div [(make-map add [(outsmap :o0) (outsmap :o1)] []) [2]] [:o2])]
   [:o0 :o2 :o1]))

(println "c " outsmap)
(println (min-max-avg [1,2,3,4,5]))
(println (min-max-avg [30,40,80]))

(println "c " outsmap)