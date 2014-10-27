import wx,wx.html

class AboutInfo(wx.Dialog):
    """ class for banner display """
    text = '''
<html>
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0"
cellpadding="0" border="1">
<tr>
<td align="center"><h1>C source to PDF utility (C2PDF)</h1></td>
</tr>
</table>
</center>
<h3>
<p><b>C2PDF(Version 1.02, 2014.10.22)</b> is a tool for <b>converting C source files to a PDF file</b>. 
 It is developed with wxPython by Lu.
 
</p>
<p><b>C2PDF</b> Copyright 2012-2014 Lu.  All rights reserved.

</p>
<p>Permission to use in the <i>Programming Principles & C </i>course
for grade 2014, department of computer science and technology <b>only</b>!!!

</p>
</h3>
</body>
</html>
'''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "About C2PDF",size=(600, 400))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "Ok")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

