#-*-coding: utf-8-*-

# renderPDF - draws Drawings onto a canvas

#__version__=''' $Id: renderPDF.py 3959 2012-09-27 14:39:39Z robin $ '''
#__doc__="""显示画图对象 within others PDFs or standalone

import wx,time,os
#from reportlab.graphics.shapes import _baseGFontName, _baseGFontNameBI

from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFont
#from reportlab.platypus import tableofcontents
#from reportlab.lib.styles import ParagraphStyle as PS
#from reportlab.lib.units import inch
#from reportlab.tools.docco.rl_doc_utils import *
#from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import pdfencrypt
from os.path import basename
from reportlab.pdfgen.canvas import Canvas





##
###from reportlab.graphics.shapes import *
##from reportlab.pdfbase.pdfmetrics import stringWidth
##from reportlab.lib.utils import getStringIO
##from reportlab import rl_config
##from reportlab.graphics.renderbase import Renderer, StateTracker, getStateDelta, renderScaledDrawing
##
##
### the main entry point for users...
##def draw(drawing, canvas, x, y, showBoundary=rl_config._unset_):
##    """As it says"""
##    R = _PDFRenderer()
##    R.draw(renderScaledDrawing(drawing), canvas, x, y, showBoundary=showBoundary)
##
##class _PDFRenderer(Renderer):
##    """This draws onto a PDF document.  It needs to be a class
##    rather than a function, as some PDF-specific state tracking is
##    needed outside of the state info in the SVG model."""
##
##    def __init__(self):
##        self._stroke = 0
##        self._fill = 0
##        self._tracker = StateTracker()
##
##        dt = MyFileDropTarget(self)
##        self.SetDropTarget(dt)
##
##
##    def drawNode(self, node):
##        """This is the recursive method called for each node
##        in the tree"""
##        #print "pdf:drawNode", self
##        #if node.__class__ is Wedge: stop
##        if not (isinstance(node, Path) and node.isClipPath):
##            self._canvas.saveState()
##
##        #apply state changes
##        deltas = getStateDelta(node)
##        self._tracker.push(deltas)
##        self.applyStateChanges(deltas, {})
##
##        #draw the object, or recurse
##        self.drawNodeDispatcher(node)
##
##        self._tracker.pop()
##        if not (isinstance(node, Path) and node.isClipPath):
##            self._canvas.restoreState()
##
##    def drawRect(self, rect):
##        if rect.rx == rect.ry == 0:
##            #plain old rectangle
##            self._canvas.rect(
##                    rect.x, rect.y,
##                    rect.width, rect.height,
##                    stroke=self._stroke,
##                    fill=self._fill
##                    )
##        else:
##            #cheat and assume ry = rx; better to generalize
##            #pdfgen roundRect function.  TODO
##            self._canvas.roundRect(
##                    rect.x, rect.y,
##                    rect.width, rect.height, rect.rx,
##                    fill=self._fill,
##                    stroke=self._stroke
##                    )
##
##    def drawImage(self, image):
##        path = image.path
##        # currently not implemented in other renderers
##        if path and (hasattr(path,'mode') or os.path.exists(image.path)):
##            self._canvas.drawInlineImage(
##                    path,
##                    image.x, image.y,
##                    image.width, image.height
##                    )
##
##    def drawLine(self, line):
##        if self._stroke:
##            self._canvas.line(line.x1, line.y1, line.x2, line.y2)
##
##    def drawCircle(self, circle):
##            self._canvas.circle(
##                    circle.cx, circle.cy, circle.r,
##                    fill=self._fill,
##                    stroke=self._stroke
##                    )
##
##    def drawPolyLine(self, polyline):
##        if self._stroke:
##            assert len(polyline.points) >= 2, 'Polyline must have 2 or more points'
##            head, tail = polyline.points[0:2], polyline.points[2:],
##            path = self._canvas.beginPath()
##            path.moveTo(head[0], head[1])
##            for i in range(0, len(tail), 2):
##                path.lineTo(tail[i], tail[i+1])
##            self._canvas.drawPath(path)
##
##    def drawWedge(self, wedge):
##        centerx, centery, radius, startangledegrees, endangledegrees = \
##         wedge.centerx, wedge.centery, wedge.radius, wedge.startangledegrees, wedge.endangledegrees
##        yradius, radius1, yradius1 = wedge._xtraRadii()
##        if yradius is None: yradius = radius
##        angle = endangledegrees-startangledegrees
##        path = self._canvas.beginPath()
##        if (radius1==0 or radius1 is None) and (yradius1==0 or yradius1 is None):
##            path.moveTo(centerx, centery)
##            path.arcTo(centerx-radius, centery-yradius, centerx+radius, centery+yradius,
##                   startangledegrees, angle)
##        else:
##            path.arc(centerx-radius, centery-yradius, centerx+radius, centery+yradius,
##                   startangledegrees, angle)
##            path.arcTo(centerx-radius1, centery-yradius1, centerx+radius1, centery+yradius1,
##                   endangledegrees, -angle)
##        path.close()
##        self._canvas.drawPath(path,
##                    fill=self._fill,
##                    stroke=self._stroke)
##
##    def drawEllipse(self, ellipse):
##        #need to convert to pdfgen's bounding box representation
##        x1 = ellipse.cx - ellipse.rx
##        x2 = ellipse.cx + ellipse.rx
##        y1 = ellipse.cy - ellipse.ry
##        y2 = ellipse.cy + ellipse.ry
##        self._canvas.ellipse(x1,y1,x2,y2,fill=self._fill,stroke=self._stroke)
##
##    def drawPolygon(self, polygon):
##        assert len(polygon.points) >= 2, 'Polyline must have 2 or more points'
##        head, tail = polygon.points[0:2], polygon.points[2:],
##        path = self._canvas.beginPath()
##        path.moveTo(head[0], head[1])
##        for i in range(0, len(tail), 2):
##            path.lineTo(tail[i], tail[i+1])
##        path.close()
##        self._canvas.drawPath(
##                            path,
##                            stroke=self._stroke,
##                            fill=self._fill
##                            )
##
##    def drawString(self, stringObj):
##        if self._fill:
##            S = self._tracker.getState()
##            text_anchor, x, y, text, enc = S['textAnchor'], stringObj.x,stringObj.y,stringObj.text, stringObj.encoding
##            if not text_anchor in ['start','inherited']:
##                font, font_size = S['fontName'], S['fontSize']
##                textLen = stringWidth(text, font, font_size, enc)
##                if text_anchor=='end':
##                    x -= textLen
##                elif text_anchor=='middle':
##                    x -= textLen*0.5
##                elif text_anchor=='numeric':
##                    x -= numericXShift(text_anchor,text,textLen,font,font_size,enc)
##                else:
##                    raise ValueError, 'bad value for textAnchor '+str(text_anchor)
##            t = self._canvas.beginText(x,y)
##            t.textLine(text)
##            self._canvas.drawText(t)
##
##    def drawPath(self, path):
##        from reportlab.graphics.shapes import _renderPath
##        pdfPath = self._canvas.beginPath()
##        drawFuncs = (pdfPath.moveTo, pdfPath.lineTo, pdfPath.curveTo, pdfPath.close)
##        isClosed = _renderPath(path, drawFuncs)
##        if isClosed:
##            fill = self._fill
##        else:
##            fill = 0
##        if path.isClipPath:
##            self._canvas.clipPath(pdfPath, fill=fill, stroke=self._stroke)
##        else:
##            self._canvas.drawPath(pdfPath,
##                        fill=fill,
##                        stroke=self._stroke)
##
##    def setStrokeColor(self,c):
##        self._canvas.setStrokeColor(c)
##
##    def setFillColor(self,c):
##        self._canvas.setFillColor(c)
##
##    def applyStateChanges(self, delta, newState):
##        """This takes a set of states, and outputs the PDF operators
##        needed to set those properties"""
##        for key, value in delta.items():
##            if key == 'transform':
##                self._canvas.transform(value[0], value[1], value[2],
##                                 value[3], value[4], value[5])
##            elif key == 'strokeColor':
##                #this has different semantics in PDF to SVG;
##                #we always have a color, and either do or do
##                #not apply it; in SVG one can have a 'None' color
##                if value is None:
##                    self._stroke = 0
##                else:
##                    self._stroke = 1
##                    self.setStrokeColor(value)
##            elif key == 'strokeWidth':
##                self._canvas.setLineWidth(value)
##            elif key == 'strokeLineCap':  #0,1,2
##                self._canvas.setLineCap(value)
##            elif key == 'strokeLineJoin':
##                self._canvas.setLineJoin(value)
###            elif key == 'stroke_dasharray':
###                self._canvas.setDash(array=value)
##            elif key == 'strokeDashArray':
##                if value:
##                    if isinstance(value,(list,tuple)) and len(value)==2 and isinstance(value[1],(tuple,list)):
##                        phase = value[0]
##                        value = value[1]
##                    else:
##                        phase = 0
##                    self._canvas.setDash(value,phase)
##                else:
##                    self._canvas.setDash()
##            elif key == 'fillColor':
##                #this has different semantics in PDF to SVG;
##                #we always have a color, and either do or do
##                #not apply it; in SVG one can have a 'None' color
##                if value is None:
##                    self._fill = 0
##                else:
##                    self._fill = 1
##                    self.setFillColor(value)
##            elif key in ['fontSize', 'fontName']:
##                # both need setting together in PDF
##                # one or both might be in the deltas,
##                # so need to get whichever is missing
##                fontname = delta.get('fontName', self._canvas._fontname)
##                fontsize = delta.get('fontSize', self._canvas._fontsize)
##                self._canvas.setFont(fontname, fontsize)
##            elif key=='fillOpacity':
##                if value is not None:
##                    self._canvas.setFillAlpha(value)
##            elif key=='strokeOpacity':
##                if value is not None:
##                    self._canvas.setStrokeAlpha(value)
##            elif key=='fillOverprint':
##                self._canvas.setFillOverprint(value)
##            elif key=='strokeOverprint':
##                self._canvas.setStrokeOverprint(value)
##            elif key=='overprintMask':
##                self._canvas.setOverprintMask(value)
##
##from reportlab.platypus import Flowable
##class GraphicsFlowable(Flowable):
##    """Flowable wrapper around a Pingo drawing"""
##    def __init__(self, drawing):
##        self.drawing = drawing
##        self.width = self.drawing.width
##        self.height = self.drawing.height
##
##    def draw(self):
##        draw(self.drawing, self.canv, 0, 0)
##
##def drawToFile(d, fn, msg="", showBoundary=rl_config._unset_, autoSize=1):
##    """Makes a one-page PDF with just the drawing.
##
##    If autoSize=1, the PDF will be the same size as
##    the drawing; if 0, it will place the drawing on
##    an A4 page with a title above it - possibly overflowing
##    if too big."""
##    d = renderScaledDrawing(d)
##    c = Canvas(fn)
##    if msg:
##        c.setFont(rl_config.defaultGraphicsFontName, 36)
##        c.drawString(80, 750, msg)
##    c.setTitle(msg)
##
##    if autoSize:
##        c.setPageSize((d.width, d.height))
##        draw(d, c, 0, 0, showBoundary=showBoundary)
##    else:
##        #show with a title
##        c.setFont(rl_config.defaultGraphicsFontName, 12)
##        y = 740
##        i = 1
##        y = y - d.height
##        draw(d, c, 80, y, showBoundary=showBoundary)
##
##    c.showPage()
##    c.save()
##    if sys.platform=='mac' and not hasattr(fn, "write"):
##        try:
##            import macfs, macostools
##            macfs.FSSpec(fn).SetCreatorType("CARO", "PDF ")
##            macostools.touched(fn)
##        except:
##            pass
##
##def drawToString(d, msg="", showBoundary=rl_config._unset_,autoSize=1):
##    "Returns a PDF as a string in memory, without touching the disk"
##    s = getStringIO()
##    drawToFile(d, s, msg=msg, showBoundary=showBoundary,autoSize=autoSize)
##    return s.getvalue()

def drawFooter(c,page,srcFile,no):
    #2013.10.10
    srcFile = srcFile.decode('utf8')#?
    line = "Page %d-%d     %s  :  %s    %s"%(no,page,wx.GetHostName(),wx.GetUserName(),srcFile)
    t=time.localtime()
    ctime = '%04d-%02d-%02d %02d:%02d:%02d'%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)

    c.setFont("MyFont",8)
    c.line(5, 25, 590,25)
    c.drawString(10, 10, line)
    c.drawRightString(585, 10, ctime)

    c.line(5, 810, 590,810)
    line = u"2014级程序设计原理与C语言"
    c.drawString(10, 820, line)
    line = "Principles of Programming for grade 2014"
    c.drawRightString(585, 820, line)
    
    
   
def anySplit(x,sep):
    for c in sep:
       splitpoint = x[:81].rfind(c)
       if splitpoint>=70: break
    if splitpoint<70: splitpoint=80
    return x[:splitpoint+1],x[splitpoint+1:]
    
    

#########################################################
#
#   test code.  First, define a bunch of drawings.
#   Routine to draw them comes at the end.
#
#########################################################


def test(srcFiles,values={ },passwd='C2014',outfile=None):

    srcFiles = sorted(srcFiles,key=basename)
    
    registerFont(UnicodeCIDFont('STSong-Light'))

    from reportlab.pdfbase import ttfonts
#    font = ttfonts.TTFont('MyFont', r'C:\Windows\Fonts\simhei.ttf')
    font = ttfonts.TTFont('MyFont', r'msyhbd.ttf')
#    font = ttfonts.TTFont('MyFont', 'msyhbd.ttf')
    registerFont(font)

    user = values.get('user','')
    if user: user = user.encode('utf8')
    
    name = values.get('name','').encode('utf8')

    password = values.get('passwd','')
    if password.strip(): passwd=password.encode('utf8')#?

    if values.get('lab','')!='':
      labv = int(values.get('lab','0'))
    else: labv=0
    if 0<labv<20: lab = ('Lab%d'%labv).encode('utf8')
    else: lab=u''

#    if user.startswith('10132130') and 0<labv<20:
#    2013.10.10
    if user.startswith('101') and len(user)==11 and 0<labv<20:
#    2013.10.10
#       outfile = (os.getcwd()+'/'+user.encode('utf8')+'_'+'%02d.c'%labv).encode('utf8')
                                                #?
       outfile = (os.getcwdu()+u'/'+user.encode('utf8')+u'_'+u'%02d.PDF'%labv)

    if outfile==None:

#      if srcFiles[0].rfind('.')!=-1:
#         pdffile = srcFiles[0][:srcFiles[0].rfind('.')]
#      else: pdffile = srcFiles[0]
#    2013.10.10
      bname=basename(srcFiles[0])
      if bname.rfind('.')!=-1:
         pdffile = bname[:bname.rfind('.')]
      else: pdffile = bname
      pdffile = os.getcwd()+'/'+pdffile
#    2013.10.10
      pdffile=unicode(pdffile.decode('utf8'))#?

    else:
      if outfile.rfind('.')!=-1:
         pdffile = outfile[:outfile.rfind('.')]
      else: pdffile = outfile

#    2013.10.10
#    pdffile --> pdffile.encode('gbk')

    if passwd=="C2014":    c = Canvas(pdffile.encode('utf8')+'.pdf') 
    else:
       c = Canvas(pdffile.encode('utf8')+'.pdf',\
               encrypt=pdfencrypt.StandardEncryption\
               (passwd,ownerPassword='c14c',canPrint=0,canCopy=0)) 

#    c = Canvas(pdffile+'.pdf')
    c.showOutline()
    
    c.setAuthor(u"LU")
    c.setTitle(u"2014级程序设计原理与C语言作业")
    c.setSubject(u"作业")
    c.setCreator(u"C2PDF")
    c.setKeywords(['C语言','程序设计','作业','2014级'])

    blank = "",""
    line1 = u"课程名", u"2014级程序设计原理与C语言"+'      '+u"Principles of Programming & C"
    chost = u"机器名",wx.GetHostName()
    cuser = u"用户名",wx.GetUserName()
    ID = u"学号",user
    USER = u"姓名",name
    grade = u"成绩",u" "
    labName = u"作业名",lab
    lines = (line1,chost,cuser,ID,USER,blank,labName,grade)
    
    c.setFont("MyFont",12)
    x,y,delta=50,800,20
    for line in lines:
      c.drawString(x, y, line[0])
      from reportlab.lib.colors import pink, black, red, blue, green
     
      if line[0]==u"成绩":
#        c.saveState()
        c.setFillColor(red)
        c.setFont("MyFont",20)
        y -= 15
        c.drawString(x+70, y, line[1])
        c.setFont("MyFont",12)
        c.setFillColor(black)
#        c.restoreState()
      else:
        c.drawString(x+70, y, line[1])
      y -= delta

    
    filelist=srcFiles
    s0="Table of Contents"
    c.bookmarkPage(s0,'FitH')
    c.addOutlineEntry(s0,s0)
    for no,f in enumerate(filelist):


#       c.addOutlineEntry(basename(f),f)
#       2013.10.10
       c.addOutlineEntry(basename(f).decode('utf8'),f)#?
       y -= delta
#       c.drawString(x, y, "%2d: %s"%(no+1,f))
#       2013.10.10
       c.drawString(x, y, "%2d: %s"%(no+1,f.decode('utf8')))#?
       c.linkRect("", f,(x,y+delta-5,x+400,y-5), Border='[0 0 0]')
 
    t = time.localtime()
    ctime = '%04d-%02d-%02d %02d:%02d:%02d'%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
    c.drawString(x+70, y-2*delta, ctime)

    c.showPage()


                          
    for no,f in enumerate(filelist):   outOneFile(f,c,no+1)

    """
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, Frame
    styles = getSampleStyleSheet()

    toc = TableOfContents()
    PS = ParagraphStyle
    toc.levelStyles = [
    PS(fontName='Times-Bold', fontSize=14, name='TOCHeading1',\
       leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
    PS(fontSize=12, name='TOCHeading2',\
      leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12) ]


    styleN = styles['Normal']
    styleH = styles['Heading1'] 
    styleH2 = styles['Heading2'] 
    story = [ ]

    story.append(Paragraph("This is a Heading<font size=54> abc[&alpha;] <greek>e</greek> <greek>p</greek> </font>",styleH))
    story.append(Spacer(inch,inch))
    story.append(Paragraph("This is a paragraph in <i>Normal</i> style.", styleN))
    story.append(Paragraph("This is a Heading2 style.", styleH2))
    toc.addEntry(0, 'txt', 1)
    toc.addEntry(1, 'txt1', 2)
    
    story.append(toc)
    f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1)
    f.addFromList(story,c)
    """
    c.save()
#    print 'saved PDF file for '+pdffile

    return pdffile+u'.pdf'
  

def outOneFile(srcFile,c,no):

    c.bookmarkPage(srcFile,'FitH')

    c.setFont("MyFont", 18)
    
    c.drawString(10, 780, 'Code Listing')

    from reportlab.graphics import testshapes
    drawings =[]
    for i,line in enumerate(open(srcFile)):
       line="%3d:    %s"%( i+1, line.rstrip('\n'))
       try:
         x=line.decode('utf8')
       except:
           x=line.decode('gbk')

       first=True
       while len(x)>85:
          r = anySplit(x,''' ,=;'"+-*/)''')
          drawings.append(r[0])
          x=' '*10+r[1]
         
       drawings.append(x)

    y = 770
    i = 1
    page = 0
    for line in drawings:
        if y < 50:  #allows 5-6 lines of text
            page+=1
            drawFooter(c,page,srcFile,no) 
            c.showPage()
            y = 800
        y = y - 18
        c.setFont("MyFont",12)
        c.drawString(10, y, line)

        i = i + 1
    if y!=800:
        page+=1
        drawFooter(c,page,srcFile,no) 
        c.showPage()


if __name__=='__main__':
    srcFiles = (r"renderpdf.py","help.txt")
    outfile = r"renderpdf.pdf"
    test(srcFiles,outfile=outfile)

