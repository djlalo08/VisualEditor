(defmacro do-horizontal [& stmts]
  `(do ~@stmts))

(defmacro do-vertical [& stmts]
  `(do ~@stmts))

(def outsmap {})

(defn output [name value]
  (def outsmap (assoc outsmap name value)))

(defn make-map [map-name [& inputs] [& outputs]]
  (println)
  (println "---- " map-name " ----")
  (println inputs)
  (let [results (apply map-name inputs)]
    (println "res " results)
    (doseq [zipped (map vector outputs results)]
      (output (zipped 0) (zipped 1))
      (println outsmap))
    ((vector [results]) 0)))

  ;; (doseq [result (apply map-name [inputs]) output-name [outputs]]
    ;; (println result output-name)))
    ;; (output output-name result)))

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
                   [2]
                   ] [:o2]))
   (vector (outsmap :o0) (outsmap :o1) (outsmap :o2))))


;; (println (div [12 13 14] [1 2 3]))
(println "output: " (x))
;; (make-map min-max [[1,2,3,4,5]] [:o0 :o1])
;; (def y (make-map min-max [1,2,3,4,5] [:o0 :o1]))
;; (println "y: " y)
;; (make-map div [[12, 10] [2]] [:_ :_])
(println outsmap)
;; println (make-map min-max [,3,4,5] [:o0 :o1])
;; (println (min-max [1,2,3,4,5]))