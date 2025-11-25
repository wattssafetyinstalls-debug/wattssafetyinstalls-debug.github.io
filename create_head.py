# create_head.py
def create_head(page_title):
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - Watts Safety Installs</title>
    <meta name="description" content="Professional {page_title} services in Norfolk, NE. Quality workmanship and reliable service for all your home improvement needs.">
    
    <!-- CSS -->
    <style>
        /* Reset and base styles */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        
        /* Header styles */
        header {{ background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: fixed; width: 100%; top: 0; z-index: 1000; }}
        .nav-container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; height: 70px; }}
        .logo img {{ height: 50px; }}
        .nav-menu {{ display: flex; list-style: none; }}
        .nav-menu li {{ position: relative; margin-left: 20px; }}
        .nav-menu a {{ text-decoration: none; color: #333; padding: 10px; display: block; }}
        .nav-dropdown:hover .dropdown {{ display: block; }}
        .dropdown {{ display: none; position: absolute; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 200px; list-style: none; }}
        .dropdown li {{ margin: 0; }}
        .dropdown a {{ padding: 10px 15px; white-space: nowrap; }}
        
        /* Main content */
        .main-content {{ margin-top: 70px; min-height: calc(100vh - 140px); padding: 40px 20px; max-width: 1200px; margin-left: auto; margin-right: auto; }}
        
        /* Footer styles */
        footer {{ background: #333; color: white; padding: 40px 0 20px; }}
        .footer-container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }}
        .footer-section h3 {{ margin-bottom: 15px; color: #fff; }}
        .footer-section ul {{ list-style: none; }}
        .footer-section ul li {{ margin-bottom: 8px; }}
        .footer-section a {{ color: #ccc; text-decoration: none; }}
        .footer-section a:hover {{ color: white; }}
        .footer-bottom {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #555; }}
        
        /* Service page styles */
        .service-title {{ font-size: 2.5em; margin-bottom: 20px; color: #2c3e50; }}
        .service-description {{ font-size: 1.1em; margin-bottom: 30px; line-height: 1.8; }}
        .back-button {{ display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-bottom: 30px; }}
        .back-button:hover {{ background: #2980b9; }}
    </style>
    
    <!-- JavaScript for pretty URLs -->
    <script>
    const redirects = {{
        '/driveway-installation': '/services/driveway-installation.html',
        '/concrete-pouring': '/services/concrete-pouring.html',
        '/hardwood-flooring': '/services/hardwood-flooring.html',
        '/garden-maintenance': '/services/garden-maintenance.html',
        '/landscape-design': '/services/landscape-design.html',
        '/painting-services': '/services/painting-services.html',
        '/snow-removal': '/services/snow-removal.html',
        '/custom-cabinets': '/services/custom-cabinets.html',
        '/deck-construction': '/services/deck-construction.html',
        '/home-remodeling': '/services/home-remodeling.html'
    }};
    
    const currentPath = window.location.pathname;
    if (redirects[currentPath]) {{
        window.location.href = redirects[currentPath];
    }}
    </script>
</head>'''
    return head