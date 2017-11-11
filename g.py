from tkinter import *

def dbg(text):  print (text, file= sys.stderr)

def domain(mainframeclass, palette= None):
  global root
  root = Tk()
  root.palette= palette;  root.bgcolor= 'gray'
  mw= mainframeclass(root)
  mw.populate()
  mw.pack(fill=BOTH,expand=True)
  root.mainloop()

def killmain():
  global root
  try:  root.destroy()
  except:  pass
  root= None

#-----------------------------------------------------------------

class packframe(Frame):
  def __init__(self, parent, palette= None, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    self.root = parent
    self.palette= palette;  self.bgcolor= 'lightgray'
    if palette== None:  self.palette= root.palette
    self.choosebg('bgcolframe')

  def choosebg(self, key):
    palette= self.palette
    if palette== None:  return
    if not (key in palette):  return
    bgcolor= palette[key];  self.bgcolor= bgcolor
    self.configure(bg= bgcolor)

  # the "parent" to feed tkinter when creating sub-widgets
  def tktarget(self):  return self

  def populate(self):    return

  def title(self, title):   self.root.title(title)

  def label(self, text, white= False, **kwargs):
    bgcolor= self.bgcolor
    tkw= Label(self.tktarget(), text= text, bg= bgcolor)
    if white:  tkw.config(fg= 'white')
    self.tktarget().packw(tkw, fill=X, expand= False, **kwargs)

  def wlabel(self, text, **kwargs):  self.label(text, white= True, **kwargs)

  def button(self, text, command, **kwargs):
    tkw= Button(self.tktarget(), text=text, command=command)
    self.tktarget().packw(tkw, expand= False, **kwargs)

  def okbutton(self, text= 'OK', **kwargs):
    global root
    tkw= self.button(text, self.on_ok, **kwargs)
    root.bind("<Return>", self.on_ok)

  def entry(self, width=30, colspan=1, text=''):
    tkw= Entry(self.tktarget(), width=width)
    self.tktarget().packw(tkw, colspan=colspan, fill=X)
    tkw.insert(0, text)
    return tkw

  def packw(self, tkw, **kwargs):
    fill= BOTH;  expand= True
    if 'expand' in kwargs:  expand= kwargs['expand']
    if 'fill' in kwargs:  fill= kwargs['fill']
    tkw.pack(fill= fill, side=TOP, expand= expand)

  def subframe(self, sfclass):
    sf= sfclass(self)
    sf.populate(); self.packw(sf)
    return sf

  def vscrollsubframe(self, viewclass):
    scr= vscrollframe(self)
    scr.viewclass= viewclass
    scr.populate(); self.packw(scr)
    return scr.viewclass

#--------------------------------------------------------------------

class gridframe(packframe):
  def __init__(self, parent, *args, **kwargs):
    packframe.__init__(self, parent, *args, **kwargs)
    self.row= 0;  self.col= 0
    self.choosebg('bggrid')
 
  def packw(self, tkw, **kwargs):
    colspan= 1;  sticky= 'w'
    if 'colspan' in kwargs:  colspan= kwargs['colspan']
    if 'sticky' in kwargs:  sticky= kwargs['sticky']
    tkw.grid(column=self.col, row= self.row, sticky=sticky, columnspan=colspan)
    tkw.grid_configure(padx=3, pady=3)
    self.col= self.col+ colspan

  def newrow(self):
    self.row= self.row+1; self.col= 0

class vscrollframe(packframe):
  interior= None

  def populate(self):
      # https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df
      # create a canvas object and a vertical scrollbar for scrolling it
      vscrollbar = Scrollbar(self, orient= VERTICAL)
      vscrollbar.pack(fill= Y, side= RIGHT, expand= FALSE)
      canvas = Canvas(self, bd=0, highlightthickness= 0, yscrollcommand= vscrollbar.set)
      canvas.pack(side= LEFT, fill= BOTH, expand= TRUE)
      vscrollbar.config(command= canvas.yview)

      # reset the view
      canvas.xview_moveto(0);   canvas.yview_moveto(0)

      # create a frame inside the canvas which will be scrolled with it
      self.interior = interior = self.viewclass(canvas)
      interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

      # track changes to the canvas and frame width and sync them,
      # also updating the scrollbar
      def _configure_interior(event):
        # update the scrollbars to match the size of the inner frame
        size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
        canvas.config(scrollregion="0 0 %s %s" % size)
        if interior.winfo_reqwidth() != canvas.winfo_width():
          # update the canvas's width to fit the inner frame
          canvas.config(width=interior.winfo_reqwidth())
      interior.bind('<Configure>', _configure_interior)

      def _configure_canvas(event):
        if interior.winfo_reqwidth() != canvas.winfo_width():
          # update the inner frame's width to fill the canvas
          canvas.itemconfigure(interior_id, width=canvas.winfo_width())
      canvas.bind('<Configure>', _configure_canvas)

      self.interior.populate();

  # the "parent" to feed tkinter when creating sub-widgets
  def tktarget(self):
    if self.interior:  return self.interior
    return self


 
