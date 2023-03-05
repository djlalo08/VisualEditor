export const ex = `Root
    Vertical
        Horizontal
            Map[name:a, fileinput:t]
                Ins
                Outs
                    Node
            Map[name:bbb, fileinput:t]
                Ins
                Outs
                    Node[setvalue:b]
            Map[name:c, fileinput:t]
                Ins
                Outs
                    Node[setvalue:c]
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
                                                Node[getvalue:b]
                                            Outs
                                    Node
                                        Vertical
                                            Map[name: WW]
                                                Ins
                                                    Node[getvalue:b]
                                                Outs
                                                    Node
                                            Horizontal
                                                Map[name:*, infix:true]
                                                    Ins[infix:true]
                                                        Node
                                                            Map[name:4, className:constant]
                                                        Node
                                                        Node[getvalue:c]
                                                    Outs[infix:true]
                                                        Node[setvalue:1]
                                                Vertical
                                                    Horizontal
                                                        Map[name:Z]
                                                            Ins
                                                            Outs
                                                                Node[setvalue:2]
                                                    Horizontal
                                                        Map[name:ZZ]
                                                            Ins
                                                            Outs
                                            Map[name:W]
                                                Ins
                                                    Node[getvalue:1]
                                                    Node[getvalue:2]
                                Outs[infix:true]
                    Outs
                        Node[setvalue:discr]
                Vertical
                    Horizontal
                        Map[name:X, className:constant]
                    Horizontal
                        Map[name:Y, className:constant]
            Horizontal
                Map[name:123]
                    Ins
                        Node[getvalue:discr]
                        Node
                            Map[name:"x", className:constant]
                    Outs
                        Node[setvalue:end]
        Horizontal
            Map[name:, fileoutput:t]
                Ins
                    Node[getvalue:end]
                Outs`