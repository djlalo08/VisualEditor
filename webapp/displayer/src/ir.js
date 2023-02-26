export const ex = `Root
    Horizontal
        FileInput
        FileInput
            SetNode[value:b, x:True]
        FileInput
            SetNode[value:c, x:True]
    Vertical
        Map[name:sqrt]
            Ins
                Node
                    Map[name:-, infix:true]
                        Ins[infix:true]
                            Node
                                Map[name:sqr]
                                    Ins
                                        Node
                                            GetNode[value:b]
                                    Outs
                            Node
                                Map[name:*, infix:true]
                                    Ins[infix:true]
                                        Node
                                            Map[name:4, className:constant]
                                        Node
                                        Node
                                            GetNode[value:c]
                                    Outs[infix:true]
                        Outs[infix:true]
            Outs
                Node
                    SetNode[value:discr]
    Horizontal
        FileOutput
            GetNode[value:discr, x:True]`