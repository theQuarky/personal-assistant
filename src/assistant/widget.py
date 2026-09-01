import tkinter as tk
from tkinter import ttk
from assistant.db import list_tasks, workload

def run():
    root=tk.Tk(); root.title('Personal Assistant'); root.geometry('760x430'); root.minsize(600,320)
    ttk.Label(root,text='PERSONAL ASSISTANT',font=('TkDefaultFont',16,'bold')).pack(anchor='w',padx=18,pady=(16,4))
    summary=ttk.Label(root); summary.pack(anchor='w',padx=18,pady=(0,12))
    frame=ttk.Frame(root); frame.pack(fill='both',expand=True,padx=18)
    tree=ttk.Treeview(frame,columns=('id','priority','due','minutes','task'),show='headings')
    for c,text,w in (('id','ID',45),('priority','Priority',70),('due','Due',150),('minutes','Time',70),('task','Task',360)):
        tree.heading(c,text=text); tree.column(c,width=w,anchor='w')
    tree.pack(fill='both',expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for t in list_tasks(): tree.insert('', 'end', values=(t['id'],t['priority'],t['due_at'] or '—',f"{t['duration_minutes']}m",t['title']))
        w=workload(); summary.config(text=f"Open tasks: {w['task_count']}    Planned work: {w['planned_hours']}h")
    ttk.Button(root,text='Refresh',command=refresh).pack(anchor='e',padx=18,pady=14)
    refresh(); root.mainloop()
if __name__=='__main__': run()
