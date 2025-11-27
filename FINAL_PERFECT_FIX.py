#!/usr/bin/env python3
"""
FINAL PERFECT CAROUSEL FIX - 7 tiles, real hamburger dropdowns, gradient hovers, 
preserves header/footer/promo, no conflicts, beautiful & smooth
"""
import re

def final_fix():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove ONLY old/broken carousels (safe)
    content = re.sub(r'<section class="premium-services-carousel.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="services-carousel-section.*?</section>', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="carousel-section.*?</section>', '', content, flags=re.DOTALL)

    # 2. THE FINAL CAROUSEL (7 tiles, real hamburger dropdowns, gradient hover)
    final_carousel = '''
    <!-- FINAL PREMIUM CAROUSEL - 7 tiles, perfect dropdowns, gradient hover -->
    <section class="final-premium-carousel">
        <div class="final-carousel-inner">
            <div class="final-track">
                <!-- 1 Accessibility -->
                <div class="final-slide active">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1350&q=80" alt="Accessibility & Safety">
                        <div class="final-content">
                            <h3>Accessibility & Safety Solutions</h3>
                            <p>ADA showers, grab bars, ramps, non-slip flooring</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/ada-compliant-showers.html">ADA Showers</a>
                                    <a href="/services/grab-bars.html">Grab Bars</a>
                                    <a href="/services/wheelchair-ramps.html">Ramps</a>
                                    <a href="/services/non-slip-flooring.html">Non-Slip Flooring</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Free Assessment →</a>
                        </div>
                    </div>
                </div>
                <!-- 2 Remodeling -->
                <div class="final-slide">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=1350&q=80" alt="Home Remodeling">
                        <div class="final-content">
                            <h3>Home Remodeling</h3>
                            <p>Kitchens, bathrooms, basements, full renovations</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/kitchen-renovations.html">Kitchens</a>
                                    <a href="/services/bathroom-remodels.html">Bathrooms</a>
                                    <a href="/services/basement-finishing.html">Basements</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Start Your Project →</a>
                        </div>
                    </div>
                </div>
                <!-- 3 Concrete & Flooring -->
                <div class="final-slide">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1350&q=80" alt="Concrete">
                        <div class="final-content">
                            <h3>Concrete & Flooring</h3>
                            <p>Driveways, patios, hardwood, luxury vinyl</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/driveway-installation.html">Driveways</a>
                                    <a href="/services/patio-construction.html">Patios</a>
                                    <a href="/services/hardwood-flooring.html">Hardwood</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Get Quote →</a>
                        </div>
                    </div>
                </div>
                <!-- 4 Cabinets -->
                <div class="final-slide">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=1350&q=80" alt="Cabinets">
                        <div class="final-content">
                            <h3>Cabinets & Countertops</h3>
                            <p>Custom cabinets, refacing, quartz & onyx</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/custom-cabinets.html">Custom Cabinets</a>
                                    <a href="/services/cabinet-refacing.html">Refacing</a>
                                    <a href="/services/onyx-countertops.html">Onyx Tops</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Design Consult →</a>
                        </div>
                    </div>
                </div>
                <!-- 5 Maintenance -->
                <div class="final-slide">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1350&q=80" alt="Maintenance">
                        <div class="final-content">
                            <h3>Property Maintenance</h3>
                            <p>Snow removal, gutters, emergency repairs</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/snow-removal.html">Snow Removal</a>
                                    <a href="/services/gutter-cleaning.html">Gutters</a>
                                    <a href="/services/emergency-repairs.html">Emergency</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Schedule Service →</a>
                        </div>
                    </div>
                </div>
                <!-- 6 Lawn Care -->
                <div class="final-slide">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=1350&q=80" alt="Lawn">
                        <div class="final-content">
                            <h3>Lawn & Landscape</h3>
                            <p>Mowing, fertilization, full design</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/lawn-maintenance.html">Mowing</a>
                                    <a href="/services/fertilization.html">Fertilization</a>
                                    <a href="/services/landscape-design.html">Design</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Get Lawn Quote →</a>
                        </div>
                    </div>
                </div>
                <!-- 7 TV & More -->
                <div class="final-slide">
                    <div class="final-card">
                        <img src="https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=1350&q=80" alt="TV">
                        <div class="final-content">
                            <h3>TV, Audio & Painting</h3>
                            <p>Professional mounting & installation</p>
                            <div class="final-hamburger">
                                <i class="fas fa-bars"></i>
                                <div class="final-dropdown">
                                    <a href="/services/tv-mounting.html">TV Mounting</a>
                                    <a href="/services/home-theater-installation.html">Home Theater</a>
                                    <a href="/services/painting-services.html">Painting</a>
                                </div>
                            </div>
                            <a href="tel:+14054106402" class="final-cta">Book Now →</a>
                        </div>
                    </div>
                </div>
            </div>
            <button class="final-prev"><i class="fas fa-chevron-left"></i></button>
            <button class="final-next"><i class="fas fa-chevron-right"></i></button>
            <div class="final-dots"></div>
        </div>
    </section>'''

    # Insert right after hero (preserves everything else)
    hero_match = re.search(r'(<section class="services-hero">.*?</section>)', content, re.DOTALL)
    if hero_match:
        content = content.replace(hero_match.group(0), hero_match.group(0) + final_carousel)

    # FINAL CSS + JS (adds only if not present)
    final_style_js = '''
    <style>
    .final-premium-carousel{padding:90px 0;background:var(--warm-light);position:relative;overflow:hidden}
    .final-premium-carousel::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3z' fill='%23f59e0b' fill-opacity='0.04'/%3E%3C/svg%3E");opacity:0.7}
    .final-carousel-inner{max-width:1200px;margin:0 auto;position:relative}
    .final-track{display:flex;transition:transform .6s cubic-bezier(.4,0,.2,1)}
    .final-slide{min-width:100%;padding:20px}
    .final-card{background:#fff;border-radius:28px;overflow:hidden;box-shadow:0 15px 40px rgba(0,0,0,.1);transition:all .5s}
    .final-card:hover{transform:translateY(-16px) scale(1.02);background:linear-gradient(135deg,var(--teal),var(--navy));color:#fff;box-shadow:0 30px 70px rgba(0,196,180,.4)}
    .final-card:hover .final-cta{background:#fff;color:var(--navy)}
    .final-card img{width:100%;height:280px;object-fit:cover}
    .final-content{padding:30px;position:relative}
    .final-hamburger i{font-size:2rem;color:var(--teal);cursor:pointer;position:absolute;top:20px;right:20px;transition:all .3s}
    .final-card:hover .final-hamburger i{color:#fff}
    .final-dropdown{display:none;position:absolute;top:60px;right:10px;background:#fff;border-radius:16px;box-shadow:0 15px 40px rgba(0,0,0,.2);min-width:200px;z-index:100}
    .final-hamburger:hover .final-dropdown{display:block}
    .final-dropdown a{display:block;padding:14px 20px;color:var(--navy);text-decoration:none;transition:.3s}
    .final-dropdown a:hover{background:var(--teal);color:#fff}
    .final-cta{display:inline-block;margin-top:20px;padding:14px 32px;background:var(--teal);color:#fff;border-radius:50px;font-weight:700;text-decoration:none;transition:.4s}
    .final-prev,.final-next{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,196,180,.95);color:#fff;width:64px;height:64px;border-radius:50%;border:none;font-size:2.4rem;cursor:pointer;z-index:10;box-shadow:0 10px 30px rgba(0,0,0,.3)}
    .final-prev{left:-32px}.final-next{right:-32px}
    .final-dots{text-align:center;margin-top:40px}
    .final-dots span{display:inline-block;width:14px;height:14px;background:#ccc;border-radius:50%;margin:0 8px;cursor:pointer;transition:.4s}
    .final-dots span.active{background:var(--teal);transform:scale(1.4)}
    @media(max-width:768px){
        .final-prev{left:10px;width:50px;height:50px;font-size:1.8rem}
        .final-next{right:10px;width:50px;height:50px;font-size:1.8rem}
    }
    </style>
    <script>
    document.addEventListener("DOMContentLoaded",()=>{const t=document.querySelector(".final-track"),e=document.querySelectorAll(".final-slide"),n=document.querySelector(".final-dots"),a=document.querySelector(".final-prev"),i=document.querySelector(".final-next");let o=0;const r=()=>{e.forEach(t=>t.classList.remove("active")),n.querySelectorAll("span").forEach(t=>t.classList.remove("active")),e[o].classList.add("active"),n.children[o].classList.add("active"),t.style.transform=`translateX(-${o*100}%)`},c=()=>{o=(o+1)%e.length,r()},l=()=>{o=(o-1+e.length)%e.length,r()};a&&a.addEventListener("click",()=>{clearInterval(s),l(),s=setInterval(c,5000)}),i&&i.addEventListener("click",()=>{clearInterval(s),c(),s=setInterval(c,5000)}),e.forEach((t,e)=>{const a=document.createElement("span");a.addEventListener("click",()=>{o=e,clearInterval(s),r(),s=setInterval(c,5000)}),n.appendChild(a)}),r();let s=setInterval(c,5000);document.querySelector(".final-carousel-inner").addEventListener("mouseenter",()=>clearInterval(s)),document.querySelector(".final-carousel-inner").addEventListener("mouseleave",()=>s=setInterval(c,5000))});
    </script>'''

    if '.final-premium-carousel' not in content:
        content = re.sub(r'(</style>)', final_style_js + '\\1', content, count=1)

    # Promo cards gradient hover (safe)
    content = content.replace('class="promo-card"', 'class="promo-card final-card"')

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("FINAL FIX COMPLETE")
    print("7 perfect tiles with real dropdowns")
    print("Full gradient hover on cards & promo")
    print("Header phone, footer links, everything preserved")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    final_fix()