#_*_coding:utf-8_*_

import _fontdata_enc_macexpert
import _fontdata_enc_macroman
import _fontdata_enc_pdfdoc
import _fontdata_enc_standard
import _fontdata_enc_symbol
import _fontdata_enc_winansi
import _fontdata_enc_zapfdingbats
import _fontdata_widths_courier
import _fontdata_widths_courierbold
import _fontdata_widths_courierboldoblique
import _fontdata_widths_courieroblique
import _fontdata_widths_helvetica
import _fontdata_widths_helveticabold
import _fontdata_widths_helveticaboldoblique
import _fontdata_widths_helveticaoblique
import _fontdata_widths_symbol
import _fontdata_widths_timesbold
import _fontdata_widths_timesbolditalic
import _fontdata_widths_timesitalic
import _fontdata_widths_timesroman
import _fontdata_widths_zapfdingbats





from renderPDF import test
from aboutBox import AboutInfo
import wx,os,time,tempfile,os.path,pickle
#from ModalLessPDF import PDF
from os.path import basename
import os
import webbrowser

class MyFileDropTarget(wx.FileDropTarget):
  def __init__(self, window):
    wx.FileDropTarget.__init__(self)
    self.window = window
  def OnDropFiles(self, x, y, filenames):
    
#    srcFiles = [x.encode('utf8') for x in set(self.window.srcFiles+filenames)]
#    2013.10.10

    self.window.srcFiles= [x.decode('utf8') for x in self.window.srcFiles]

    srcFiles = [x.encode('utf8') for x in set(self.window.srcFiles+filenames)]

    srcFiles = sorted(srcFiles,key=basename)

    self.window.srcFiles = srcFiles
    self.window.Refresh()
    
def fileExist(fname,response='Y'):
    """ check if a file exists or not  """
    if not os.path.exists(fname):
        if response=='Y': print("File {:s} does't exist".format(fname))
        return False
    return True

def LoadINI():
    """ initialization   """
    iniFile = os.environ['HOME']+'/c2pdf.ini'
    param = {'user': wx.GetUserName(),'lab':'1'}

    if fileExist(iniFile,'N'):  
#       for line in open(iniFile,'r'):
#          s = line.split('=')
#          param[s[0].rstrip(' ')] = s[1].strip(' ').rstrip('\n')
      f = open(iniFile,'r')
      for x,y in pickle.load(f).items():  param[x]=y
    
    return param

def SaveINI(param):

#    print(param)
    
    iniFile = os.environ['HOME']+'/c2pdf.ini'
    f = open(iniFile,'w')
#    for k in ('user','name','passwd','lab'):
#        if k in param and param[k]:
#            f.write('{:s} = {:s}\n'.format(k,param[k].encode('cp936')))
    pickle.dump(param,f,pickle.HIGHEST_PROTOCOL)
    f.close()


class ConfigDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self, parent, -1, 'Config Dialog',size=(300, 200))
    self.values = parent.values

    panel             = wx.Panel(self)
    topLbl           = wx.StaticText(panel, -1, "Configuration")
    topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    
    userLbl         = wx.StaticText(panel, -1, "UseID:")
    self.user       = wx.TextCtrl(panel, -1, self.values.get('user',''));
    nameLbl       = wx.StaticText(panel, -1, "Name:")
    self.name     = wx.TextCtrl(panel, -1, self.values.get('name',''))
    passwdLbl   = wx.StaticText(panel, -1, "Password:")
    self.passwd = wx.TextCtrl(panel, -1, self.values.get('passwd',''))
    labLbl           = wx.StaticText(panel, -1, "Lab#:")
    self.lab         = wx.TextCtrl(panel, -1, self.values.get('lab',''))

#  2013.10.10
#   pdfreaderLbl   = wx.StaticText(panel, -1, "PDF Reader:")
#    self.pdfreader = wx.TextCtrl(panel, -1, self.values.get('pdfreader',''))


#    outfileLbl = wx.StaticText(panel, -1, "PDF:")
#    outfile = wx.StaticText(panel, -1, "")

    okButton = wx.Button(panel, -1, "OK")    
    cancelButton = wx.Button(panel, -1, "Cancel")
    # Now do the layout.
    # mainSizer is the top-level one that manages everything
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(topLbl, 0, wx.ALL, 5)
    mainSizer.Add(wx.StaticLine(panel), 0,wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

    userSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
    userSizer.AddGrowableCol(1)
    userSizer.Add(userLbl, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    userSizer.Add(self.user, 0, wx.EXPAND)
    userSizer.Add(nameLbl, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    userSizer.Add(self.name, 0, wx.EXPAND)
    userSizer.Add(passwdLbl, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    userSizer.Add(self.passwd, 0, wx.EXPAND)
    userSizer.Add(labLbl, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    userSizer.Add(self.lab, 0, wx.EXPAND)

    #  2013.10.10
#    userSizer.Add(pdfreaderLbl, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
#    userSizer.Add(self.pdfreader, 0, wx.EXPAND)


#    userSizer.Add(outfileLbl, 0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
#    userSizer.Add(outfile, 0, wx.EXPAND)
    userSizer.Add((10,10)) # some empty space

    # now add the userSizer to the mainSizer
    mainSizer.Add(userSizer, 0, wx.EXPAND|wx.ALL, 10)
    # The buttons sizer will put them in a row with resizeable
    # gaps between and on either side of the buttons
    btnSizer = wx.BoxSizer(wx.HORIZONTAL)
    btnSizer.Add((60,60), 1)
    btnSizer.Add(okButton)
    btnSizer.Add((60,60), 1)
    btnSizer.Add(cancelButton)
    btnSizer.Add((60,20), 1) 
    mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
 
    panel.SetSizer(mainSizer)
    # Fit the frame to the needs of the sizer. The frame will
    # automatically resize the panel as needed. Also prevent the
    # frame from getting smaller than this size.
    mainSizer.Fit(self)
    mainSizer.SetSizeHints(self)

    self.Bind(wx.EVT_BUTTON, self.OnOK, okButton)
    self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)

  def OnOK(self, evt):
    if self.user.GetValue():
        self.values['user'] = self.user.GetValue().strip(' ')
    if self.name.GetValue():
       self.values['name'] = self.name.GetValue().strip(' ')
#2013.10.10
#    if self.passwd.GetValue():
    if True:
       self.values['passwd'] = self.passwd.GetValue().strip(' ')
    if self.lab.GetValue():
       self.values['lab'] = self.lab.GetValue().strip(' ')

    #  2013.10.10
#    if True:
#       self.values['pdfreader'] = self.pdfreader.GetValue().strip(' ')

       
    self.GetParent().values = self.values
    self.Close()
    SaveINI(self.values)

  def OnCancel(self, evt):
    self.Close()

  def getValue(self):
   return  self.values


class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, u"C2PDF", size=(900, 600))
    self.SetBackgroundColour('white')
    tmpfile=tempfile.mktemp()+'.ico'
    import icon
    icon.icon.GetImage().SaveFile(tmpfile,wx.BITMAP_TYPE_ICO)
    self.SetIcon(wx.Icon(name=tmpfile, type=wx.BITMAP_TYPE_ICO))

    self.SetMenuBar(self.CreateMenu())
    self.CreateStatusBar()
   
    self.Bind(wx.EVT_MENU, self.OnClose, id=self.IDM_EXIT)
    self.Bind(wx.EVT_CLOSE, self.OnExit)

    self.Bind(wx.EVT_MENU, self.OnOpen, id=self.IDM_OPEN)
#    self.Bind(wx.EVT_MENU, self.OnOpenPDF, id=self.IDM_OPENPDF)
    self.Bind(wx.EVT_MENU, self.OnBuild, id=self.IDM_BUILD)
    self.Bind(wx.EVT_MENU, self.OnConfig, id=self.IDM_CONFIG)
    self.Bind(wx.EVT_MENU, self.OnAbout, id=self.IDM_ABOUT)
    self.Bind(wx.EVT_MENU, self.OnHelp, id=self.IDM_HELP)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.wx.EVT_CONTEXT_MENU, self.OnShowPopup)

    self.srcFiles = [ ]
    self.outfile = None
    self.PDFWindow  = None
    self.popupmenu = self.CreatePopupMenu()
    self.values = LoadINI()
    self.pos = None

    """
    import win32con
    self.F5 = wx.NewId()
    self.RegisterHotKey(self.F5,win32con.MOD_CONTROL,win32con.VK_F5)
    self.Bind(wx.EVT_HOTKEY, self.OnHotKey,id=self.F5)

    self.F1 = wx.NewId()
    self.RegisterHotKey(self.F1,win32con.MOD_CONTROL,win32con.VK_F1)
    self.Bind(wx.EVT_HOTKEY, self.OnHotKey,id=self.F1)
    """

    dt = MyFileDropTarget(self)
    self.SetDropTarget(dt)


  def OutFile(self):
    user = self.values.get('user','')
    if user: user = user.encode('utf8')
    if self.values.get('lab','')!='':
      labv = int(self.values.get('lab','0'))
    else: labv=0
    if 0<labv<20: lab = ('Lab%d'%labv).encode('utf8')
    else: lab=u''
#    if user.startswith('10132130') and 0<labv<20:
#    2013.10.10
    if user.startswith('101') and len(user)==11 and 0<labv<20:
#    2013.10.10
#       outfile = (os.getcwd()+'/'+user.encode('gbk')+'_'+'%02d.PDF'%labv).encode('utf8')
       outfile = (os.getcwdu()+u'/'+user.encode('utf8')+u'_'+u'%02d.PDF'%labv)

       return outfile
    return None

  def OnConfig(self, event):
    dialog = ConfigDialog(self)
    result = dialog.ShowModal()
#    wx.MessageBox("Dialog value is '%s'" % str(self.values), "Dialog Result", wx.OK | wx.ICON_INFORMATION, self)
    dialog.Destroy()
    self.outfile = self.OutFile()
    self.Refresh()
    

  def CreatePopupMenu(self):
    menuBar = wx.Menu()
#    self.IdCommand = wx.NewId()
#    2013.10.10
    self.IdCommand = self.IDM_DELETE
    menuBar.Append(self.IdCommand, u"删除", "unselect this file")
    self.Bind(wx.EVT_MENU, self.OnCommand, id=self.IdCommand)
    return menuBar

  def OnShowPopup(self, event):
    pos = event.GetPosition()
    pos = self.ScreenToClient(pos)
    self.pos = pos
    self.PopupMenu(self.popupmenu,pos)
    
  def OnCommand(self, evt):
    
      if self.pos:
        idx=(self.pos.y-60)/30
        if idx< len(self.srcFiles): del self.srcFiles[idx]
        self.Refresh()
      evt.Skip()  

  def OnHotKey(self, evt):
        self.SetFocus()
        if evt.GetId()==self.F1:    self.OnHelp(evt)
        if evt.GetId()==self.F5:    self.OnBuild(evt)

  def CreateMenu(self):
    self.IDM_EXIT=100
    self.IDM_OPEN=101
    self.IDM_OPENPDF=104
    self.IDM_BUILD=102
    self.IDM_CONFIG=105

    self.IDM_ABOUT=401
    self.IDM_HELP=402
    
    #2013.10.10
    self.IDM_DELETE=911


    self.menuBar = wx.MenuBar()

    menu = wx.Menu()
    menu.Append(self.IDM_CONFIG, u"设置...", "Config")
    menu.AppendSeparator()

    menu.Append(self.IDM_OPEN, u"打开(&O)\tCtrl+O", "Select source File")
    menu.Append(self.IDM_BUILD, u"生成PDF", "Build PDF")
    menu.AppendSeparator()
#    menu.Append(self.IDM_OPENPDF, u"OpenPDF", "Open PDF")
#    menu.AppendSeparator()
    menu.Append(self.IDM_EXIT, u"退出(&X)\tCtrl+X", "Exit")
    self.menuBar.Append(menu, u"文件(&F)")
    menu = wx.Menu()
    menu.Append(self.IDM_HELP, u"?", "Help\tF1")
    menu.Append(self.IDM_ABOUT, u"程序信息(&I)", "Program Info")
    self.menuBar.Append(menu, u"关于(&A)")

    return self.menuBar

  def OnSize(self, evt):
    self.Refresh()

  def OnBuild(self, evt):
    if self.srcFiles:
      self.outfile = test(self.srcFiles,self.values)
      wx.MessageBox(u"打开PDF文件检查生成的结果:\n  "+self.outfile,u"信息", wx.OK , self)
      self.OnOpenPDF(evt)
    else: wx.MessageBox(u"没有选择文件",u"错误", wx.OK , self)
    self.Refresh()

  def OnPaint(self, evt):
   dc=wx.PaintDC(self)
   dc.Clear()
   self.w,self.h=dc.GetSize()
   font=wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD, False)
   dc.SetFont(font)
   dc.DrawText(u"PDF文件: %s"%self.outfile,10,10)
   dc.SetBrush(wx.Brush("#0",wx.TRANSPARENT))
   dc.DrawRectangle(10,60,self.w-20,self.h-70)
   if self.srcFiles:  self.DrawFilenames(dc,self.srcFiles,15,65)
    
  def DrawFilenames(self,dc,srcFiles,x,y):
     for i,fn in enumerate(srcFiles):
        dc.DrawText('%d: %s'%(i+1,fn),x,y)
        y += 30
   
  def OnOpenPDF(self, evt):
     if self.outfile: 
        webbrowser.open(self.outfile)
     evt.Skip()

  def OnOpen(self, evt):
    wildcard ="C Files(*.c)|*.c|All Files(*.*)|*.*"
    dialog = wx.FileDialog(self, "select a file", os.getcwd(),"", wildcard, wx.OPEN|wx.MULTIPLE)
    filenames = [ ]
    if dialog.ShowModal() == wx.ID_OK:  filenames = dialog.GetPaths()
    dialog.Destroy()  

#   srcFiles = [x.encode('utf8') for x in set(self.srcFiles+filenames)]
 #    2013.10.10
    self.srcFiles = [x.decode('utf8') for x in self.srcFiles]
    
    srcFiles = [x.encode('utf8') for x in set(self.srcFiles+filenames)]
    srcFiles = sorted(srcFiles,key=basename)

    self.srcFiles = srcFiles
    self.Refresh()

  def OnAbout(self, evt):
#      wx.MessageBox(u"C文件转换成PDF文件", "C2PDF", wx.OK | wx.ICON_INFORMATION, self)
        dlg=AboutInfo(self)
        dlg.ShowModal()
        dlg.Destroy()

  def OnHelp(self, evt):
      
 #     wx.MessageBox(u"C文件转换成PDF文件", "C2PDF", wx.OK | wx.ICON_INFORMATION, self)
        helpfile = os.getcwd()+'/help.pdf'
        webbrowser.open(helpfile)
        """        
        if self.PDFWindow==None:
            self.PDFWindow = PDF(self)
            wx.BeginBusyCursor()
            self.PDFWindow.pdf.LoadFile(helpfile)
            wx.EndBusyCursor()
            self.PDFWindow.Show()
        else:
            wx.BeginBusyCursor()
            self.PDFWindow.pdf.LoadFile(helpfile)
            wx.EndBusyCursor()
        self.PDFWindow.SetTitle(helpfile)
        """
	
  def OnClose(self, evt):
    if self.PDFWindow:   self.PDFWindow.Destroy()

    self.Close()


  def OnExit(self, evt):
    if self.PDFWindow:   self.PDFWindow.Destroy()

    self.Destroy()


app = wx.PySimpleApp()
frame = MyFrame()
frame.Show(True)
app.MainLoop()
