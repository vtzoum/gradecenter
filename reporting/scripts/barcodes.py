#!/usr/bin/env python
from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
 
#----------------------------------------------------------------------
def createBarCodes():
    """
    Create barcode examples and embed in a PDF
    """
    c = canvas.Canvas("barcodes.pdf", pagesize=letter)
 
    barcode_value = [
        '0004-0000000001', '0004-0000000002','0004-0000000003','0004-0000000004','0004-0000000005',
        '0004-0000000013','0004-0000000028','0004-0000000029','0004-0000000030','0004-0000000031',
    ]
    #barcode_value = "1234567890"
    barcode_value = "0004-0000000001"
 
    barcode39 = code39.Extended39(barcode_value, humanReadable=True)
    barcode39Std = code39.Standard39(barcode_value, barHeight=20, stop=1, humanReadable=True)
 
    # code93 also has an Extended and MultiWidth version
    barcode93 = code93.Standard93(barcode_value, humanReadable=True)
 
    barcode128 = code128.Code128(barcode_value, humanReadable=True)
    # the multiwidth barcode appears to be broken 
    #barcode128Multi = code128.MultiWidthBarcode(barcode_value)
 
    barcode_usps = usps.POSTNET("50158-9999")
 
    codes = [barcode39, barcode39Std, barcode93, barcode128, barcode_usps]
 
    x = 1 * mm
    y = 285 * mm
    x1 = 6.4 * mm
 
    for code in codes:
        code.drawOn(c, x, y)
        y = y - 15 * mm
 
    # draw the eanbc8 code
    """
    barcode_eanbc8 = eanbc.Ean8BarcodeWidget(barcode_value)
    bounds = barcode_eanbc8.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(50, 10)
    d.add(barcode_eanbc8)
    renderPDF.draw(d, c, 15, 555)
    """
 
    # draw the eanbc13 code
    """
    barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
    bounds = barcode_eanbc13.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(50, 10)
    d.add(barcode_eanbc13)
    renderPDF.draw(d, c, 15, 465)
    """
 
    c.save()
 
if __name__ == "__main__":
    createBarCodes()
