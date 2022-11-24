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
  (vector (apply + 
                 as)))

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

(defn m [metadata value] value)

(defx
  min-max-avg
  [(m {"name" "ls"} [:ix]) [:i1 :i0]]
  [(make-map min-max [(outsmap :i0)] [:o0 :o1])
   (m {"infix" "true"} (make-map / [(m {"infix" "true"} (make-map + [(outsmap :o0) (outsmap :o1)] [])) (m {"constant" "true"} [2])] [:o2]))]
  [(m {"name" "min"} [:o0]) (m {"name" "avg"} [:o2, :o1]) (m {"name" "max"} [:o1])])

(defx
  min-max-avg-no-m
  [[:ix] [:i1 :i0]]
  [(make-map min-max [(outsmap :i0)] [:o0 :o1])
   (make-map / [(make-map + [(outsmap :o0) (outsmap :o1)] [])  [2]] [:o2])]
  [[:o0] [:o2, :o1] [:o1]])

;; (println (make-map + [12 4] []))


(defx 
  quadratic
  [[:a] [:b] [:c]]
  [(make-map sqrt [(m {"infix" "true"} (make-map - [(make-map sqr [(outsmap :b)] [])
                                                    (m {"infix" "true"} (make-map * [(m {"className" "constant"} [4]) (outsmap :a) (outsmap :c)] []))]
                                                 []))]
             [:discr])]
  [[:discr]])

(defx
  quadratic
  [[:a] [:b] [:c]]
  [(make-map sqrt [(make-map - 
                             [(make-map sqr [(outsmap :b)] []) 
                              (make-map * [[4] (outsmap :a) (outsmap :c)] [])]
                             [])]
             [:discr])]
  [[:discr]])

;; (defx
  ;; square
  ;; [[:x]]
  ;; [(make-map sqr [(outsmap :x)] [:x2])]
  ;; [:x2])

;; (println (macroexpand '(defx
                        ;;  square
                        ;;  [[:x]]
                        ;;  [(make-map sqr [(outsmap :x)] [:x2])]
                        ;;  [:x2])))

;; (def square 
  ;; (fn [& in-vals] 
    ;; (do 
      ;; (read-inputs [[:x]] in-vals) 
      ;; (doseq [line [(make-map sqr [(outsmap :x)] [:x2])]] 
        ;; (list line)) 
      ;; (map (fn [x] (map outsmap x)) [:x2]))))

(def outsmap (assoc outsmap :a 3))
(def outsmap (assoc outsmap :b 20))
(def outsmap (assoc outsmap :c 2))
(println "before " outsmap)

(println (make-map + [8 2] [:r]))
(println "after " outsmap)


(println (make-map sqr [(outsmap :b)] [:b2]))
(println (make-map * [4 (outsmap :a) (outsmap :c)] [:4ac]))
(make-map - [8 2]
          [:res])
;; (make-map sqr [(outsmap :x)] [:x2])
;; (make-map * [4 (outsmap :a) (outsmap :c)] [:res])

(println "after " outsmap)


;; (println (min-max-avg [[1,2,3,4,5]] [[0,0,0] [10,20,30,40]]))
;; (println (min-max-avg [[30,40,80]] [[][300,400,800]]))
(println "result " (square [4]))


(require '[clojure.core.match :refer [match]])


(defn combine-destruct [in-names in-values]
  (map pair in-names in-values))


(println (pair :i0 5))
(println (pair [:i0 [:i1 :i2 [:a :b [:c :d]]]] [0 [1 2 [\a \b [\c \d]]]]))


;; (println (combine-destruct :i0 0))

(comment 
  "I think it is important and maybe necessary to do the whole everything-returns-a-list thing. I think we need to really think about how we're going to do types before we make it hard to change things to work with what we have.
   
   I'm thinking: everything is list. Every item is actually a list of length 1 . So if we do (+ 1 2 3 4) that's really the same as (+ [1] [2] [3] [4]) which in turn 'unpacks' every item.
   
   The big issue is 'are the situations where the programmer might actually *want* single-item lists? We should make it possible to still do this...
")