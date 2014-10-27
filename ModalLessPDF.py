#_*_coding:utf-8_*_

import wx
import wx.lib.pdfwin

class PDF(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self, parent, -1, 'View PDF',size=(1200, 700),pos=(100,10), 
            style=wx.DEFAULT_FRAME_STYLE&~wx.MINIMIZE_BOX)

    bx=wx.BoxSizer(wx.VERTICAL)
    self.pdf = wx.lib.pdfwin.PDFWindow(self, style=wx.SUNKEN_BORDER)
    bx.Add(self.pdf, proportion=1, flag=wx.EXPAND)
    self.SetSizer(bx)
    self.Bind(wx.EVT_CLOSE, self.OnCancel)

  def OnCancel(self, evt):
    self.Destroy()
    self.GetParent().PDFWindow=None
