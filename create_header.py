# create_header.py
def create_header():
    header = '''<header>
    <nav>
        <div class="nav-container">
            <div class="logo">
                <a href="index.html">
                    <img src="images/logo.png" alt="Watts Safety Installs" width="200" height="60">
                </a>
            </div>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li class="nav-dropdown">
                    <a href="services.html">Services</a>
                    <ul class="dropdown">
                        <li><a href="/driveway-installation">Driveway Installation</a></li>
                        <li><a href="/concrete-pouring">Concrete Pouring</a></li>
                        <li><a href="/hardwood-flooring">Hardwood Flooring</a></li>
                        <li><a href="/garden-maintenance">Garden Maintenance</a></li>
                        <li><a href="/landscape-design">Landscape Design</a></li>
                        <li><a href="/painting-services">Painting Services</a></li>
                        <li><a href="/snow-removal">Snow Removal</a></li>
                        <li><a href="/custom-cabinets">Custom Cabinets</a></li>
                        <li><a href="/deck-construction">Deck Construction</a></li>
                        <li><a href="/home-remodeling">Home Remodeling</a></li>
                    </ul>
                </li>
                <li><a href="service-area.html">Service Area</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="referrals.html">Referrals</a></li>
                <li><a href="contact.html">Contact</a></li>
            </ul>
        </div>
    </nav>
</header>'''
    return header