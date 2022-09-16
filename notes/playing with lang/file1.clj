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

;; (println (div [10 20 30] [1 2 6]))

(defn add [& as]
  (vector (apply + as)))


(defn pair_ [a b]
  (if (vector? a)
    (mapcat pair_ a b)
    [a b]))

(defn pair [a b] (partition 2 (pair_ a b)))

(defn read-inputs [input-names input-values]
  (let [r (pair input-names input-values)]
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


(defn !m [metadata value] value)

(println
 (defx
   min-max-avg
   [(!m {"input-name" "ls"} [:ix]) (!m {"input-name" "unused"} [:i1 :i0])]
   [(make-map min-max [(outsmap :i0)] [:o0 :o1])
    (make-map div [(make-map add [(outsmap :o0) (outsmap :o1)] []) [2]] [:o2])]
   [:o0 :o2 :o1]))

(println "c " outsmap)

(println (min-max-avg [[1,2,3,4,5]] [[0,0,0] [10,20,30,40]]))
(println (min-max-avg [[30,40,80]] [[][300,400,800]]))

(println "c " outsmap)

(require '[clojure.core.match :refer [match]])


(defn combine-destruct [in-names in-values]
  (map pair in-names in-values))


(println (pair :i0 5))
(println (pair [:i0 [:i1 :i2 [:a :b [:c :d]]]] [0 [1 2 [\a \b [\c \d]]]]))


;; (println (combine-destruct :i0 0))