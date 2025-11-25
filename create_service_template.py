# create_service_template.py
from create_head import create_head
from create_header import create_header
from create_footer import create_footer

def create_service_page(service_slug, service_title, service_description, services_list):
    print(f"Creating service page: {service_slug}")
    
    head = create_head(service_title)
    header = create_header()
    footer = create_footer()
    
    # Create services list HTML
    services_html = "<ul>"
    for service in services_list:
        services_html += f"<li>{service}</li>"
    services_html += "</ul>"
    
    page_content = f'''{head}
<body>
    {header}
    
    <main class="main-content">
        <a href="../services.html" class="back-button">← Back to All Services</a>
        
        <h1 class="service-title">{service_title}</h1>
        
        <div class="service-description">
            <p>{service_description}</p>
        </div>
        
        <div class="services-list">
            <h2>Our {service_title} Services Include:</h2>
            {services_html}
        </div>
        
        <div class="cta-section">
            <h2>Ready to Get Started?</h2>
            <p>Contact us today for a free consultation and estimate!</p>
            <a href="../contact.html" class="back-button">Contact Us</a>
        </div>
    </main>
    
    {footer}
</body>
</html>'''
    
    return page_content