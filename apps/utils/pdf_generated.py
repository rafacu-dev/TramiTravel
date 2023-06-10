

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import gray,black,HexColor
from core import settings
from django.core.files.storage import FileSystemStorage

def style(fontName="Helvetica-Bold",alignment=TA_CENTER,fontSize=11,spaceBefore=4):
    return ParagraphStyle(name="estiloEncabezado", alignment=alignment,fontSize=fontSize, textColor=black, fontName=fontName,parent= getSampleStyleSheet()["Normal"],spaceBefore=spaceBefore)


def generate_tickets_pdf(bookings,name):
    ttColor = HexColor(0xE5DCED)
    
    # Define la ruta absoluta de la carpeta 'media'
    media_root = str(settings.MEDIA_ROOT)

    # Concatena el nombre del archivo al final de la ruta
    file_path = media_root + f'/{name}.pdf'

    # Crea un objeto de almacenamiento de sistema de archivos
    fs = FileSystemStorage()
    
    doc = SimpleDocTemplate(file_path, leftMargin= 10*mm, rightMargin= 10*mm, topMargin = 20*mm, bottomMargin = 20*mm, pagesize = A4, title="Reporte PDF", author="TramiTravel")
    ancho, alto = doc.pagesize
    story=[]

    styleCenter = ParagraphStyle(name="estiloEncabezado", alignment=TA_CENTER,fontSize=11, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)
    styleCenterLigt = ParagraphStyle(name="estiloEncabezado", alignment=TA_CENTER,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)
    styleLeft = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)
    styleLeftLigt = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=9, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)


    img = Image("static/images/transparent.png")
    img.drawHeight = 16 * mm
    img.drawWidth = 40 * mm

    pnr = "  Pending"
    if bookings[0].pnr != None:
        pnr = str(bookings[0].pnr)
        
    row = [
        [[Paragraph("RESERVATION CODE", style(fontName="Helvetica",alignment=TA_LEFT,fontSize=8))],[Paragraph(pnr, style(alignment=TA_LEFT,fontSize=16,spaceBefore=2)),]],
        [[Paragraph("PREPARED BY", style(fontName="Helvetica"))],[Paragraph("TRAMITRAVEL", style()),]],
        img
    ]
    
    data = []
    data.append(row)
    styles = [
        ("BACKGROUND", (0, 0),(-1, 0), ttColor),
        ("ALIGN", (0,0),(-1, 0), "RIGHT"),
        ("VALIGN", (0,0),(-1, 0), "TOP"),
        ("TOPPADDING", (0,0),(-1, 0),10),
        ("BOTTOMPADDING", (0,0),(-1, 0),10),
        ("RIGHTPADDING", (0,0),(-1, 0),10)
    ]

    table = Table(data = data,style = styles, colWidths=((ancho - (10*mm * 2)) / 3), hAlign="CENTER")
    story.append(table)
    
    for booking in bookings:
        spacer = Spacer(50, 15)
        story.append(spacer)

        styles = [
            ("BACKGROUND", (0, 0),(-1, 0), ttColor),
            ("ALIGN", (0,0),(-1, 0), "RIGHT"),
            ("VALIGN", (0,0),(-1, -1), "TOP"),
            ("LINEABOVE", (0, 0), (-1, 0), 0.25, black),
            ("LINEBEFORE", (1, 0), (-1, -1), 0.1, gray)
        ]
        
        data = [
            [Paragraph("Passenger Name:", styleLeftLigt), Paragraph("Seat:", styleLeftLigt), Paragraph("TramiTravel Reservation Code:", styleLeftLigt)],
            [Paragraph(">> " + booking.name(), styleLeftLigt), Paragraph("Check-In Required", styleLeftLigt), Paragraph(str(booking.reservationCode), styleLeftLigt)],
        ]
        table = Table(data = data,style = styles, colWidths=((ancho - (10*mm * 2)) / 3), hAlign="CENTER")
        story.append(table)
        
        img = Image("static/images/avion.png")
        img.drawHeight = 12 * mm
        img.drawWidth = 12 * mm
        data = [
            [
                img,
                Paragraph("DEPARTURE: ", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                Paragraph(booking.flight.date.strftime("%A, %b %d"), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"])), 
                Paragraph("Please verify flight times prior to departure", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=gray, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"]))
            ],
        ]
        
        styles = [
            ("VALIGN", (0,0),(-1, -1), "MIDDLE"),
        ]
        table = Table(data = data,style = styles, colWidths=[14 * mm, 30 * mm,40 * mm,100 * mm], hAlign="LEFT",vAlign="TOP")
        story.append(table)
        
        spacer = Spacer(50, 5)
        story.append(spacer)
        
        img = Image("static/images/bg-tickets-bottom.png")
        img.drawHeight = 5 * mm
        img.drawWidth = 5 * mm
        
        styles = [
            ("VALIGN", (0,0),(-1, -1), "TOP"),
            ("LINEBEFORE", (1, 1), (-1, -1), 0.1, gray),
            ("LINEABOVE", (0, 1), (-1, 1), 0.1, gray)
        ]

        img_charter = Image("media/" + str(bookings[0].flight.charter.image))
        img_charter.drawHeight = 10 * mm
        img_charter.drawWidth = 15 * mm
        styles_table_img = [
            ("ALIGN", (0,0),(-1, -1), "RIGHT"),
            ("VALIGN", (0,0),(-1, -1), "TOP"),
        ]
        data = [
            [
                [
                    Paragraph(booking.flight.begin.cityCode, ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=13, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(booking.flight.begin.city + ", " + booking.flight.begin.countryCode, ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=12, textColor=black, fontName="Times-Roman",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)), 
                ],
                [
                    Paragraph(booking.flight.to.cityCode, ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=13, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(booking.flight.to.city + ", " + booking.flight.to.countryCode, ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=12, textColor=black, fontName="Times-Roman",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)), 
                ]
            ],
            [
                [
                    Paragraph("Departing At:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(booking.flight.departure.strftime("%I:%M %p").lower(), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=16, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"],spaceBefore=2)), 
                ],
                [
                    Paragraph("Arriving At:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(booking.flight.arrival.strftime("%I:%M %p").lower(), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=16, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"],spaceBefore=2)), 
                ]
            ],
            [
                [
                    Paragraph("Check-in", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(booking.flight.checkin().strftime("%I:%M %p").lower(), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=2)), 
                ],
                [
                    Paragraph("Duration:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(booking.flight.duration(), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=2)), 
                ],
            ],
        ]
        table = Table(data = data,style = styles, colWidths=(ancho - (10*mm * 2)) * 0.22,rowHeights= 14 * mm, hAlign="LEFT",vAlign="MEDIUM")

        if booking.flight.charter:
            charter = "&nbsp;&nbsp;&nbsp;" + booking.flight.charter.__str__()
        else:charter = ""


        status = "  Pending"
        if booking.pnr != None:
            status = "SUCCESS"
        data = [
            [
                [
                    Table(data = [[Paragraph(charter + "\n\n" + "&nbsp;&nbsp;&nbsp;" + booking.flight.aircraft.carrier_code.nameCode + "&nbsp;" + booking.flight.number, style(alignment=TA_LEFT,fontSize=11, fontName="Helvetica")), img_charter, ],
                                ],style = styles_table_img, hAlign="LEFT",vAlign="MEDIUM"),
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Operated By:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=12)),  
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + booking.flight.aircraft.carrier_code.__str__(), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Status", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=12)),  
                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {status}", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=9, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),
                    img,
                ],
                table,
                [
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Aircraf", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=10, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {booking.flight.aircraft.make} {booking.flight.aircraft.model}", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=10, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)), 

                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Gate: {booking.flight.gate}", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=10, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=12)),  

                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Class:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=10, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=12)),  
                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {booking.flight.class_type.name_es}", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=10, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),

                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href='http://localhost:8000/baggage-policy/{booking.flight.baggagePolicy.id}'><font color='blue'>Baggage policy here</font></a>", 
                              ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=8, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=8)), 
                ],
            ],
        ]
        
        styles = [
            ("BACKGROUND", (0, 0),(0, 0), ttColor),
            ("VALIGN", (0,0),(-1, -1), "TOP"),
            ("TOPPADDING", (0,0),(-1, 0),5),
            ("BOTTOMPADDING", (0,0),(-1, 0),0),
            ("LEFTPADDING", (0,0),(-1, 0),0),
            ("BOX", (1, 0), (-1, -1), 0.25, black),
            ("LINEBEFORE", (-1, 0), (-1, -1), 0.1, gray)
        ]
        table = Table(data = data,style = styles, colWidths=[(ancho - (10*mm * 2)) * 0.285, (ancho - (10*mm * 2)) * 0.44, (ancho - (10*mm * 2)) * 0.26], hAlign="LEFT",vAlign="MEDIUM")
        story.append(table)

    spacer = Spacer(50, 15)
    story.append(spacer)

    styles = [
        ("BACKGROUND", (0, 0),(0, 0), ttColor),
        ("TOPPADDING", (0,0),(-1,-1),35),
        ("LINEABOVE", (0, 0), (-1, 0), 0.25, black),
    ]
    table = Table(data = [""],style = styles, colWidths= ancho - (10*mm * 2), hAlign="LEFT",vAlign="MEDIUM")
    story.append(table)

    doc.build(story)


        
    # Guarda el archivo en el sistema de archivos
    with open(file_path, 'rb') as pdf:
        fs.save(f'{name}.pdf', pdf)