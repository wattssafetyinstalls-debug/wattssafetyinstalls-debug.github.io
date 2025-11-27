#!/usr/bin/env python3
"""
FINAL PERFECT CAROUSEL FIX - Safe, clean, keeps everything you love
"""
import re

def final_fix():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # === STEP 1: Remove only old/broken carousel sections safely ===
    # This removes any section that has "carousel" in the class but keeps everything else
    content = re.sub(r'<section[^>]*class="[^"]*carousel[^"]*"[^>]*>.*?</section>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # === STEP 2: Find where to insert (right after the hero section) ===
    hero_match = re.search(r'(<section class="services-hero"[\s\S]*?</section>)', content, re.IGNORECASE)
    if not hero_match:
        print("Could not find hero section - aborting")
        return

    # === STEP 3: The PERFECT carousel using YOUR existing service cards ===
    perfect_carousel = '''
    <!-- PREMIUM 7-TILE CAROUSEL - Uses your exact design, hover, dropdowns -->
    <section class="premium-service-carousel">
        <div class="carousel-outer">
            <div class="carousel-inner">
                <div class="carousel-track">
                    {}
                </div>
            </div>
            <button class="carousel-btn prev" aria-label="Previous">‹</button>
            <button class="carousel-btn next" aria-label="Next">›</button>
            <div class="carousel-indicators"></div>
        </div>
    </section>'''.format(''.join([
        f'''
        <div class="carousel-slide{' active' if i==0 else ''}">
            {card}
        </div>''' for i, card in enumerate(re.findall(r'<div class="service-card"[\s\S]*?</div>\s*</div>\s*</div>', content))
    ]))

    # === STEP 4: Insert it safely after hero ===
    content = content.replace(hero_match.group(0), hero_match.group(0) + perfect_carousel)

    # === STEP 5: Add ONLY the needed CSS/JS (no duplicates, no conflicts) ===
    css_js_addition = '''
<style>
.premium-service-carousel {padding:90px 0;background:var(--warm-light);position:relative;text-align:center}
.carousel-outer {max-width:1200px;margin:0 auto;position:relative}
.carousel-inner {overflow:hidden;border-radius:28px;box-shadow:0 20px 60px rgba(0,0,0,0.1)}
.carousel-track {display:flex;transition:transform 0.6s cubic-bezier(0.4,0,0.2,1)}
.carousel-slide {min-width:100%;padding:20px}
.carousel-btn {position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,196,180,0.95);color:white;width:64px;height:64px;border-radius:50%;border:none;font-size:36px;cursor:pointer;z-index:10;transition:all .3s;box-shadow:0 8px 25px rgba(0,0,0,0.2)}
.carousel-btn:hover {background:var(--navy);transform:translateY(-50%) scale(1.1)}
.prev {left:15px}
.next {right:15px}
.carousel-indicators {margin-top:30px}
.carousel-indicators span {display:inline-block;width:14px;height:14px;background:#ccc;border-radius:50%;margin:0 8px;cursor:pointer;transition:all .3s}
.carousel-indicators span.active {background:var(--teal);transform:scale(1.4)}
@media(max-width:768px){.carousel-btn{width:50px;height:50px;font-size:28px}}
</style>
<script>
document.addEventListener("DOMContentLoaded",()=>{const t=document.querySelector(".carousel-track"),e=document.querySelectorAll(".carousel-slide"),n=document.querySelector(".carousel-indicators"),c=document.querySelector(".prev"),i=document.querySelector(".next");let a=0,r=setInterval(()=>{a=(a+1)%e.length,o(a)},5000);const o=t=>{e.forEach(e=>e.classList.remove("active")),n.querySelectorAll("span").forEach(e=>e.classList.remove("active")),e[t].classList.add("active"),n.children[t].classList.add("active"),t.style.transform=`translateX(-${t*100}%)`};e.forEach((e,t)=>{const c=document.createElement("span");c.addEventListener("click",()=>{a=t,clearInterval(r),o(a),r=setInterval(()=>{a=(a+1)%e.length,o(a)},5000)}),n.appendChild(c)}),c&&c.addEventListener("click",()=>{clearInterval(r),a=(a-1+e.length)%e.length,o(a),r=setInterval(()=>{a=(a+1)%e.length,o(a)},5000)}),i&&i.addEventListener("