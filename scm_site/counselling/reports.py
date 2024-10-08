from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from .models import User, ChoiceEntry
from time import gmtime, strftime


class PreferenceListReport:
    def __init__(self, user: User):
        self.user = user

    def as_bytes(self):
        buffer = BytesIO()
        left_margin = 18
        right_margin = 18
        name = self.user.get_full_name()
        username = self.user.username
        report_generation_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        doc = SimpleDocTemplate(
            buffer,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=9,
            bottomMargin=9,
            title=f"Course report for {username} {name}",
        )

        # Fetch choices for the logged-in user
        choices = ChoiceEntry.objects.filter(student=self.user.student).order_by(
            "priority"
        )
        number_of_choices = choices.count()

        # Prepare data for the table
        data = [
            [
                ("Preference"),
                ("College Code"),
                ("College Name"),
                ("Course Code"),
                ("Course Name"),
            ]
        ]  # Header row

        table_style = ParagraphStyle(name="TableStyle", fontSize=10)

        for i, choice in enumerate(choices):
            program = choice.program
            course = program.course
            college = program.college
            data.append(
                [
                    Paragraph("%s" % (i + 1), style=table_style),
                    Paragraph(college.code, style=table_style),
                    Paragraph(f'{college.name}, {college.city}', style=table_style),
                    Paragraph(course.code, style=table_style),
                    Paragraph(course.name, style=table_style),
                ]
            )

        # Create the table
        column_widths = [1 * inch, 1 * inch, 2.5 * inch, 1 * inch, 2.5 * inch]
        table = Table(data, colWidths=column_widths)
        # table.wrapOn(doc, left_margin, right_margin)

        # Add styling to the table
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header row background
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.lightgoldenrodyellow),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )

        table.setStyle(style)

        details_style = ParagraphStyle(name="DetailsStyle", fontSize=12, spaceAfter=10, fontName="Helvetica")
        # Build the document with the table
        doc.build(
            [
                Paragraph(f"Application id: {username}", style=details_style),
                Paragraph(f"Name: {name.upper()}", style=details_style),
                Paragraph(f'Report generation time: {report_generation_time}', style=details_style),
                Paragraph(f'Number of choices: {number_of_choices}', style=details_style),
                table,
            ]
        )

        # Prepare the response
        buffer.seek(0)
        return buffer
