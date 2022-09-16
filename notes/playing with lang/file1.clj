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

(def / div)

;; (println (div [10 20 30] [1 2 6]))

(defn add [& as]
  (vector (apply + as)))

(def + add)

(defn minus [& as] 
  (vector (apply - as)))

(def - minus)

(defn times [& as]
  (vector (apply * as)))

(def * times)

(defn pair_ [a b]
  (if (vector? a)
    (mapcat pair_ a b)
    [a b]))

(defn sqrt [a] 
  (let [sqrt_abs (Math/sqrt a)]
    [sqrt_abs (- sqrt_abs)]))

(defn sqr [a] (* a a))

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
                    (list 'map (list 'fn ['x] (list 'map 'outsmap 'x)) outs)))))

(println "c " outsmap)


(defn m [metadata value] value)

(defx
  min-max-avg
  [(m {"name" "ls"} [:ix]) [:i1 :i0]]
  [(make-map min-max [(outsmap :i0)] [:o0 :o1])
   (m {"infix" "true"} (make-map / [(m {"infix" "true"} (make-map + [(outsmap :o0) (outsmap :o1)] [])) (m {"constant" "true"} [2])] [:o2]))]
  [(m {"name" "min"} [:o0]) (m {"name" "avg"} [:o2, :o1]) (m {"name" "max"} [:o1])])

(defx 
  quadratic
  [[:a] [:b] [:c]]
  [(make-map sqrt [(m {"infix" "true"} (make-map - [(make-map sqr [(outsmap :b)] [])
                                                    (m {"infix" "true"} (make-map * [(m {"className" "constant"} [4]) (outsmap :a) (outsmap :c)] []))]
                                                 []))]
             [:discr])]
  [[:discr]])

(println "c " outsmap)

;; (println (min-max-avg [[1,2,3,4,5]] [[0,0,0] [10,20,30,40]]))
;; (println (min-max-avg [[30,40,80]] [[][300,400,800]]))
(println (quadratic [8] [30] [10]))

(println "c " outsmap)

(require '[clojure.core.match :refer [match]])


(defn combine-destruct [in-names in-values]
  (map pair in-names in-values))


(println (pair :i0 5))
(println (pair [:i0 [:i1 :i2 [:a :b [:c :d]]]] [0 [1 2 [\a \b [\c \d]]]]))


;; (println (combine-destruct :i0 0))