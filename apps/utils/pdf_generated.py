

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import gray,black,HexColor
from core import settings
from django.core.files.storage import FileSystemStorage


def generate_tickets_pdf(bookings,name):
    iTravelColor = HexColor(0xE5DCED)
    
    # Define la ruta absoluta de la carpeta 'media'
    media_root = str(settings.MEDIA_ROOT)

    # Concatena el nombre del archivo al final de la ruta
    file_path = media_root + f'/{name}.pdf'

    # Crea un objeto de almacenamiento de sistema de archivos
    fs = FileSystemStorage()
    
    doc = SimpleDocTemplate(file_path, leftMargin= 10*mm, rightMargin= 10*mm, topMargin = 20*mm, bottomMargin = 20*mm, pagesize = A4, title="Reporte PDF", author="TramiTravel")
    ancho, alto = doc.pagesize
    story=[]

    styleLeft = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)
    styleLeftLigt = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=9, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)


    img = Image("media/" + str(bookings[0].flight.aircraft.carrier_code.image))
    img.drawHeight = 20 * mm
    img.drawWidth = 20 * mm

    pnr = "PENDING"
    if bookings[0].pnr != None:
        pnr = str(bookings[0].pnr)
        
    row = [
        [[Paragraph(pnr, styleLeft),],[Paragraph("RESERVATION CODE", styleLeftLigt)]],
        [[Paragraph("TRAMITRAVEL SERVICES", styleLeft),],[Paragraph("GROUP CORP", styleLeft)],[Paragraph("PREPARED BY", styleLeftLigt)]],
        img
    ]
    
    data = []
    data.append(row)
    styles = [
        ("BACKGROUND", (0, 0),(-1, 0), iTravelColor),
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
            ("BACKGROUND", (0, 0),(-1, 0), iTravelColor),
            ("ALIGN", (0,0),(-1, 0), "RIGHT"),
            ("VALIGN", (0,0),(-1, -1), "TOP"),
            ("LINEABOVE", (0, 0), (-1, 0), 0.25, black),
            ("LINEBEFORE", (1, 0), (-1, -1), 0.1, gray)
        ]
        
        data = [
            [Paragraph("Passenger Name:", styleLeftLigt), Paragraph("Seat:", styleLeftLigt), Paragraph("iTravel Reservation Code:", styleLeftLigt)],
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
                Paragraph(booking.date.strftime("%A, %b %d"), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"])), 
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
            charter = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + booking.flight.charter.__str__()
        else:charter = ""


        status = "PENDING"
        if booking.pnr != None:
            status = "SUCCESS"
        data = [
            [
                [
                    Paragraph(charter, ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;" + booking.flight.aircraft.carrier_code.nameCode, ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=13, textColor=black, fontName="Helvetica-Bold",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)), 
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Operated By:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=12)),  
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + booking.flight.aircraft.carrier_code.__str__(), ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Status", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=12)),  
                    Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{status}", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=9, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),
                    img,
                ],
                table,
                [
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Aircraf", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"])), 
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Boeing 677-200", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)), 

                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Gate: G 17", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=6)),  

                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Class:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=6)),  
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Economy", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),

                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Bags Included:", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=11, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=6)),  
                    Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Handbag + Carry On", ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,fontSize=9, textColor=black, fontName="Helvetica",parent= getSampleStyleSheet()["Normal"],spaceBefore=4)),
                ],
            ],
        ]
        
        styles = [
            ("BACKGROUND", (0, 0),(0, 0), iTravelColor),
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
        ("BACKGROUND", (0, 0),(0, 0), iTravelColor),
        ("TOPPADDING", (0,0),(-1,-1),35),
        ("LINEABOVE", (0, 0), (-1, 0), 0.25, black),
    ]
    table = Table(data = [""],style = styles, colWidths= ancho - (10*mm * 2), hAlign="LEFT",vAlign="MEDIUM")
    story.append(table)

    doc.build(story)


        
    # Guarda el archivo en el sistema de archivos
    with open(file_path, 'rb') as pdf:
        fs.save(f'{name}.pdf', pdf)