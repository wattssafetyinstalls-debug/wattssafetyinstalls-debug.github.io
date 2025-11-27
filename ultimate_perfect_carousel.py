#!/usr/bin/env python3
"""
ULTIMATE PERFECT CAROUSEL - 7 tiles, gradient hovers, dropdowns, centered, professional
"""
import re

def fix_everything():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # === 1. Remove every trace of old/broken carousels ===
    content = re.sub(r'<section class="[^"]*carousel[^"]*">.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* === CLEAN SERVICE CAROUSEL.*?@media \(max-width: 480px\).*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'// Clean Service Carousel.*?</script>', '', content, flags=re.DOTALL)

    # === 2. The 7 real service tiles (with dropdowns & proper hover) ===
    carousel_html = '''
    <!-- PREMIUM SERVICE CAROUSEL - 7 tiles, gradient hover, dropdowns -->
    <section class="premium-services-carousel">
        <div class="carousel-wrapper">
            <div class="carousel-track">
                <!-- Tile 1 -->
                <div class="carousel-slide active">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Accessibility & Safety">
                        <div class="service-content">
                            <h3>Accessibility & Safety Solutions</h3>
                            <p>ADA-compliant modifications, grab bars, ramps, non-slip flooring</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/ada-compliant-showers.html">ADA Showers</a>
                                    <a href="/services/grab-bars.html">Grab Bars</a>
                                    <a href="/services/wheelchair-ramps.html">Ramps</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Call for Free Assessment</a>
                        </div>
                    </div>
                </div>
                <!-- Tile 2 -->
                <div class="carousel-slide">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Home Remodeling">
                        <div class="service-content">
                            <h3>Home Remodeling</h3>
                            <p>Kitchens, bathrooms, basements, full renovations</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/kitchen-renovations.html">Kitchens</a>
                                    <a href="/services/bathroom-remodels.html">Bathrooms</a>
                                    <a href="/services/basement-finishing.html">Basements</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Start Your Project</a>
                        </div>
                    </div>
                </div>
                <!-- Tile 3 -->
                <div class="carousel-slide">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Concrete & Flooring">
                        <div class="service-content">
                            <h3>Concrete & Flooring</h3>
                            <p>Driveways, patios, hardwood, luxury vinyl</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/driveway-installation.html">Driveways</a>
                                    <a href="/services/patio-construction.html">Patios</a>
                                    <a href="/services/hardwood-flooring.html">Hardwood</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Get Quote</a>
                        </div>
                    </div>
                </div>
                <!-- Tile 4 -->
                <div class="carousel-slide">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Cabinets">
                        <div class="service-content">
                            <h3>Cabinets & Countertops</h3>
                            <p>Custom cabinets, refacing, onyx & quartz</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/custom-cabinets.html">Custom</a>
                                    <a href="/services/cabinet-refacing.html">Refacing</a>
                                    <a href="/services/onyx-countertops.html">Onyx</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Design Consult</a>
                        </div>
                    </div>
                </div>
                <!-- Tile 5 -->
                <div class="carousel-slide">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Maintenance">
                        <div class="service-content">
                            <h3>Property Maintenance</h3>
                            <p>Snow removal, gutters, emergency repairs</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/snow-removal.html">Snow</a>
                                    <a href="/services/gutter-cleaning.html">Gutters</a>
                                    <a href="/services/emergency-repairs.html">Emergency</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Schedule</a>
                        </div>
                    </div>
                </div>
                <!-- Tile 6 -->
                <div class="carousel-slide">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Lawn Care">
                        <div class="service-content">
                            <h3>Lawn & Landscape</h3>
                            <p>Mowing, fertilization, design & install</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/lawn-maintenance.html">Mowing</a>
                                    <a href="/services/fertilization.html">Fertilization</a>
                                    <a href="/services/landscape-design.html">Design</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Get Lawn Quote</a>
                        </div>
                    </div>
                </div>
                <!-- Tile 7 -->
                <div class="carousel-slide">
                    <div class="service-card premium-hover">
                        <img src="https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80" alt="Additional">
                        <div class="service-content">
                            <h3>TV, Audio & More</h3>
                            <p>TV mounting, home theater, painting</p>
                            <div class="hamburger-menu">Menu
                                <div class="dropdown">
                                    <a href="/services/tv-mounting.html">TV Mounting</a>
                                    <a href="/services/home-theater-installation.html">Home Theater</a>
                                    <a href="/services/painting-services.html">Painting</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="cta-button">Discuss Project</a>
                        </div>
                    </div>
                </div>
            </div>

            <button class="carousel-prev"><</button>
            <button class="carousel-next">></button>
            <div class="carousel-dots"></div>
        </div>
    </section>'''

    # === 3. Insert right after hero ===
    hero_match = re.search(r'(<section class="services-hero">.*?</section>)', content, re.DOTALL)
    if hero_match:
        content = content.replace(hero_match.group(0), hero_match.group(0) + carousel_html)

    # === 4. Add premium CSS + JS (only once) ===
    premium_css_js = '''
    <style>
    .premium-services-carousel {padding:80px 0;background:var(--warm-light);position:relative;overflow:hidden}
    .premium-services-carousel::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3z' fill='%23f59e0b' fill-opacity='0.05'/%3E%3C/svg%3E");opacity:0.6}
    .carousel-wrapper{max-width:1200px;margin:0 auto;position:relative}
    .carousel-track{display:flex;transition:transform .6s ease}
    .carousel-slide{flex:0 0 100%;text-align:center}
    .service-card.premium-hover{background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.08);transition:all .4s}
    .service-card.premium-hover:hover{transform:translateY(-12px);background:linear-gradient(135deg,var(--teal),var(--navy));color:#fff;box-shadow:0 25px 50px rgba(0,196,180,.3)}
    .service-card.premium-hover:hover .cta-button{background:#fff;color:var(--navy)}
    .service-card img{width:100%;height:240px;object-fit:cover}
    .hamburger-menu{cursor:pointer;font-size:1.8rem;color:var(--teal);position:absolute;top:20px;right:20px}
    .dropdown{display:none;position:absolute;top:50px;right:0;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.15);border-radius:12px;padding:12px 0;z-index:10}
    .hamburger-menu:hover .dropdown{display:block}
    .carousel-prev,.carousel-next{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,196,180,.9);color:#fff;width:60px;height:60px;border-radius:50%;border:none;font-size:2.5rem;cursor:pointer;z-index:10}
    .carousel-prev{left:10px}.carousel-next{right:10px}
    .carousel-dots{text-align:center;margin-top:30px}
    .carousel-dots span{display:inline-block;width:12px;height:12px;background:#ccc;border-radius:50%;margin:0 6px;cursor:pointer}
    .carousel-dots span.active{background:var(--teal);transform:scale(1.3)}
    @media(max-width:768px){.carousel-prev,.carousel-next{width:50px;height:50px;font-size:2rem}}
    </style>
    <script>
    document.addEventListener('DOMContentLoaded',()=>{const e=document.querySelector('.carousel-track'),t=document.querySelectorAll('.carousel-slide'),o=document.querySelector('.carousel-dots'),n=document.querySelector('.carousel-prev'),r=document.querySelector('.carousel-next');let a=0;const l=()=>{t.forEach(e=>e.classList.remove('active')),document.querySelectorAll('.carousel-dots span').forEach(e=>e.classList.remove('active')),t[a].classList.add('active'),o.children[a].classList.add('active'),e.style.transform=`translateX(-${a*100}%)`},c=()=>{a=(a+1)%t.length,l()},i=()=>{a=(a-1+t.length)%t.length,l()};n&&n.addEventListener('click',()=>{clearInterval(s),i(),s=setInterval(c,5000)}),r&&r.addEventListener('click',()=>{clearInterval(s),c(),s=setInterval(c,5000)}),t.forEach((e,n)=>{const r=document.createElement('span');r.addEventListener('click',()=>{a=n,clearInterval(s),l(),s=setInterval(c,5000)}),o.appendChild(r)}),l();let s=setInterval(c,5000);document.querySelector('.carousel-wrapper').addEventListener('mouseenter',()=>clearInterval(s)),document.querySelector('.carousel-wrapper').addEventListener('mouseleave',()=>s=setInterval(c,5000))});
    </script>'''

    if '.premium-services-carousel' not in content:
        content = re.sub(r'(</style>)', premium_css_js + '\\1', content, count=1)

    # === 5. Fix promo cards hover too ===
    content = content.replace('class="promo-card"', 'class="promo-card premium-hover"')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("DONE - Perfect 7-tile carousel with gradient hovers, dropdowns, centered, auto-rotating")
    print("Test now: python -m http.server 8000 -> http://localhost:8000/services.html")

if __name__ == "__main__":
    fix_everything()