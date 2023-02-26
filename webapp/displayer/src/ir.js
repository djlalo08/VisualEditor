export const ex = `Root
    Horizontal
        FileInput
        FileInput
            SetNode[value:b, x:True]
        FileInput
            SetNode[value:c, x:True]
    Vertical
        Horizontal
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
                                    Vertical
                                        Horizontal
                                            Map[name:*, infix:true]
                                                Ins[infix:true]
                                                    Node
                                                        Map[name:4, className:constant]
                                                    Node
                                                    Node
                                                        GetNode[value:c]
                                                Outs[infix:true]
                                            Map[name:Z]
                                        Map[name:W]
                            Outs[infix:true]
                Outs
                    Node
                        SetNode[value:discr]
            Map[name:X, className:constant]
            Map[name:Y, className:constant]
    Horizontal
        FileOutput
            GetNode[value:discr, x:True]`