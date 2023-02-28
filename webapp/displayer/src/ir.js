export const ex = `Root
    Vertical
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
                                                        Node
                                                            SetNode[value:1]
                                                Vertical
                                                    Horizontal
                                                        Map[name:Z]
                                                            Ins
                                                            Outs
                                                                Node
                                                                    SetNode[value:2]
                                                    Horizontal
                                                        Map[name:ZZ]
                                                            Ins
                                                            Outs
                                            Map[name:W]
                                                Ins
                                                    Node
                                                        GetNode[value:1]
                                                    Node
                                                        GetNode[value:2]
                                Outs[infix:true]
                    Outs
                        Node
                            SetNode[value:discr]
                Vertical
                    Horizontal
                        Map[name:X, className:constant]
                    Horizontal
                        Map[name:Y, className:constant]
            Horizontal
                Map[name:123]
                    Ins
                        Node
                            GetNode[value:discr]
                        Node
                            Map[name:"x", className:constant]
                    Outs
                        Node
                            SetNode[value:end]
        Horizontal
            FileOutput
                GetNode[value:end, x:True]`