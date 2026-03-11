"""

PDF report generation for disease detection and recommendations.

"""



import os

from datetime import datetime

from pathlib import Path



try:

    from reportlab.lib.pagesizes import letter, A4

    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    from reportlab.lib.units import inch

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle

    from reportlab.lib import colors

    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

    HAS_REPORTLAB = True

except ImportError:

    HAS_REPORTLAB = False





class PDFReportGenerator:

    """Generate professional PDF reports for disease detection."""

    

    def __init__(self, output_dir: str = None):

        """Initialize PDF generator."""

        self.output_dir = output_dir or os.path.join(Path(__file__).parent, 'reports')

        os.makedirs(self.output_dir, exist_ok=True)

        self.available = HAS_REPORTLAB

    

    def generate_detection_report(self, detection_data: dict, image_path: str = None) -> str:

        """

        Generate comprehensive disease detection report.

        

        Args:

            detection_data: Dictionary with detection results

            image_path: Path to the scanned image

            

        Returns:

            Path to generated PDF file

        """

        if not self.available:

            raise RuntimeError("ReportLab is not installed. Install it with: pip install reportlab")

        

        from reportlab.lib.pagesizes import letter

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak

        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        from reportlab.lib import colors

        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

        from reportlab.lib.units import inch

        

        # Generate filename

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"disease_report_{timestamp}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        

        # Create PDF

        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

        story = []

        styles = getSampleStyleSheet()

        

        # Custom styles

        title_style = ParagraphStyle(

            'CustomTitle',

            parent=styles['Heading1'],

            fontSize=24,

            textColor=colors.HexColor('#2C5F2D'),

            spaceAfter=12,

            alignment=TA_CENTER

        )

        

        heading_style = ParagraphStyle(

            'CustomHeading',

            parent=styles['Heading2'],

            fontSize=14,

            textColor=colors.HexColor('#4A7C4E'),

            spaceAfter=10,

            spaceBefore=10

        )

        

        normal_style = ParagraphStyle(

            'CustomBody',

            parent=styles['BodyText'],

            fontSize=10,

            alignment=TA_JUSTIFY,

            spaceAfter=6

        )

        

        # Title

        story.append(Paragraph("ð± Plant Disease Detection Report", title_style))

        story.append(Spacer(1, 0.2*inch))

        

        # Report information

        report_info = [

            ['Report Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],

            ['Report ID:', detection_data.get('scan_id', 'N/A')],

        ]

        

        report_table = Table(report_info, colWidths=[2*inch, 4*inch])

        report_table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9')),

            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),

            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),

            ('FONTSIZE', (0, 0), (-1, -1), 10),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),

            ('GRID', (0, 0), (-1, -1), 1, colors.grey)

        ]))

        story.append(report_table)

        story.append(Spacer(1, 0.2*inch))

        

        # Detection Results

        story.append(Paragraph("Detection Results", heading_style))

        

        detection_results = [

            ['Disease Identified:', detection_data.get('disease_name', 'Unknown')],

            ['Confidence Level:', f"{detection_data.get('confidence', 0)*100:.2f}%"],

            ['Severity Level:', detection_data.get('severity_level', 'Unknown').upper()],

            ['Affected Area:', f"{detection_data.get('affected_area_percent', 0):.1f}%"]

        ]

        

        detection_table = Table(detection_results, colWidths=[2*inch, 4*inch])

        detection_table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFF9C4')),

            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#FFE082')),

            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),

            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),

            ('FONTSIZE', (0, 0), (-1, -1), 10),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),

            ('GRID', (0, 0), (-1, -1), 1, colors.grey)

        ]))

        story.append(detection_table)

        story.append(Spacer(1, 0.2*inch))

        

        # Add image if provided

        if image_path and os.path.exists(image_path):

            story.append(Paragraph("Scanned Image", heading_style))

            try:

                img = Image(image_path, width=4*inch, height=3*inch)

                story.append(img)

                story.append(Spacer(1, 0.2*inch))

            except:

                pass

        

        # Environmental Data

        env_data = detection_data.get('environmental_data', {})

        if env_data:

            story.append(Paragraph("Environmental Conditions", heading_style))

            

            env_info = [

                ['Temperature:', f"{env_data.get('temperature', 'N/A')}Â°C"],

                ['Humidity:', f"{env_data.get('humidity', 'N/A')}%"],

                ['Weather:', env_data.get('weather_condition', 'N/A')],

                ['Disease Risk Level:', env_data.get('disease_risk_level', 'N/A').upper()]

            ]

            

            env_table = Table(env_info, colWidths=[2*inch, 4*inch])

            env_table.setStyle(TableStyle([

                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#B3E5FC')),

                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),

                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),

                ('FONTSIZE', (0, 0), (-1, -1), 10),

                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),

                ('GRID', (0, 0), (-1, -1), 1, colors.grey)

            ]))

            story.append(env_table)

            story.append(Spacer(1, 0.2*inch))

        

        # Recommendations

        recommendations = detection_data.get('recommendations', {})

        if recommendations:

            story.append(Paragraph("Treatment Recommendations", heading_style))

            

            def add_key_values(data, prefix='' ):

                if isinstance(data, dict):

                    for key, value in data.items():

                        label = f"{prefix}{key.replace('_', ' ').title()}:"

                        if isinstance(value, dict):

                            add_key_values(value, prefix=f"{key.replace('_', ' ').title()} - ")

                        elif isinstance(value, list):

                            story.append(Paragraph(f"<b>{label}</b>", normal_style))

                            for item in value:

                                story.append(Paragraph(f"- {item}", normal_style))

                        elif value is not None and value != '':

                            story.append(Paragraph(f"<b>{label}</b> {value}", normal_style))



            add_key_values(recommendations)



            treatment_process = detection_data.get('complete_treatment_process', [])

            if treatment_process:

                story.append(Spacer(1, 0.1*inch))

                story.append(Paragraph("<b>Complete Treatment Process:</b>", normal_style))

                for step in treatment_process:

                    story.append(Paragraph(f"- {step}", normal_style))



            story.append(Spacer(1, 0.2*inch))

        

        # Footer

        story.append(Spacer(1, 0.3*inch))

        footer_text = (
            "This report is generated by the Smart Plant Disease Detection System. "
            "For detailed consultation, contact your local agricultural officer."
        )

        story.append(Paragraph(footer_text, ParagraphStyle(

            'Footer',

            parent=styles['Normal'],

            fontSize=8,

            textColor=colors.grey,

            alignment=TA_CENTER

        )))

        

        # Build PDF

        doc.build(story)

        return filepath

    

    def generate_summary_report(self, user_data: dict, scans_data: list) -> str:

        """

        Generate summary report with multiple scans.

        

        Args:

            user_data: User information

            scans_data: List of scan results

            

        Returns:

            Path to generated PDF file

        """

        if not self.available:

            raise RuntimeError("ReportLab is not installed")

        

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"summary_report_{timestamp}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        

        doc = SimpleDocTemplate(filepath, pagesize=letter)

        story = []

        styles = getSampleStyleSheet()

        

        # Title

        story.append(Paragraph("ð Crop Health Summary Report", styles['Title']))

        story.append(Spacer(1, 0.2*inch))

        

        # User info

        story.append(Paragraph(f"Farmer: {user_data.get('name', 'N/A')}", styles['Normal']))

        story.append(Paragraph(f"Region: {user_data.get('region', 'N/A')}", styles['Normal']))

        story.append(Spacer(1, 0.2*inch))

        

        # Scan summary

        if scans_data:

            story.append(Paragraph("Scan History", styles['Heading2']))

            

            scan_rows = [['Date', 'Disease', 'Severity', 'Confidence']]

            for scan in scans_data[-10:]:  # Last 10 scans

                scan_rows.append([

                    scan.get('timestamp', 'N/A')[:10],

                    scan.get('disease_name', 'N/A'),

                    scan.get('severity_level', 'N/A'),

                    f"{scan.get('confidence', 0)*100:.1f}%"

                ])

            

            scan_table = Table(scan_rows)

            scan_table.setStyle(TableStyle([

                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5F2D')),

                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

                ('FONTSIZE', (0, 0), (-1, 0), 10),

                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

                ('GRID', (0, 0), (-1, -1), 1, colors.black)

            ]))

            story.append(scan_table)

        

        doc.build(story)

        return filepath





# Convenience functions

def generate_disease_report(detection_data: dict, image_path: str = None) -> str:

    """Generate disease detection PDF report."""

    generator = PDFReportGenerator()

    return generator.generate_detection_report(detection_data, image_path)





def generate_farm_summary(user_data: dict, scans_data: list) -> str:

    """Generate farm summary PDF report."""

    generator = PDFReportGenerator()

    return generator.generate_summary_report(user_data, scans_data)

