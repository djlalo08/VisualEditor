import pickle
import tkinter as tk
from Canvas import Canvas
from ObjectHierarchy.Object import Object

class OpenModal(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__(Canvas.root)
        self.fn_name = tk.StringVar()
        self.open_modal()

    def submit(self):
        fn_name = self.fn_name.get()
        self.load_file(fn_name)
        self.destroy()
        
    @staticmethod
    def load_file(name):
        with open('lib/'+name, 'rb') as file:
            id_map: dict[int, Object]= pickle.load(file)
            out_ids = pickle.load(file)

        Canvas.id_map = id_map
        Canvas.out_refs = out_ids
        '''
        old_to_new_id = {}
        object_references = {}
        for id_in_old_map, obj in id_map.items():
            new_id = obj.build_obj()
            obj.id = new_id
            Canvas.id_map[new_id] = obj
            old_to_new_id[id_in_old_map] = new_id
            
            refs = obj.get_all_references()
            for ref in refs:
                if ref.id not in object_references:
                    object_references[ref.id] = []
                object_references[ref.id].append(ref)
                
        for old_id, new_id in old_to_new_id.items():
            if old_id == new_id:
                continue  
            ref_list = object_references[old_id]
            for ref in ref_list:
                if ref is None:
                    continue
                ref.id = new_id
            del object_references[old_id]

        # Canvas.outs = list(map(lambda o_id: Canvas.id_map[o_id], out_ids))
        '''
        for obj in Canvas.id_map.values():
            obj.build_obj()

        for obj in Canvas.id_map.values():
            obj.update()

        for obj in Canvas.id_map.values():
            obj.update()
            
    def open_modal(self):
        self.title("Open Map:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name).place(x = 110, y = 20)  

        submit_button = tk.Button(self, text = "Open", command=self.submit).place(x = 100, y = 60)