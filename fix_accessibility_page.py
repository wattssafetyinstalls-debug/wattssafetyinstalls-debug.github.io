#!/usr/bin/env python3
"""
Fix Broken Accessibility Page
Add missing body content to accessibility-safety-solutions page
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_accessibility_page():
    """Fix the broken accessibility page by adding missing body content"""
    
    base_dir = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec")
    accessibility_page = base_dir / "services" / "accessibility-safety-solutions" / "index.html"
    
    if not accessibility_page.exists():
        logger.error("Accessibility page not found")
        return
    
    # Read the broken page
    content = accessibility_page.read_text(encoding='utf-8', errors='ignore')
    
    # Find where head ends
    head_end = content.find('</head>')
    if head_end == -1:
        logger.error("Could not find head end")
        return
    
    # Extract head content
    head_content = content[:head_end + 7]  # Include </head>
    
    # Create body content based on working page structure
    body_content = '''
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCPM8VZ"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<header>
<div class="nav-container">
<a class="logo" href="/">WATTS</a>
<nav class="nav-links" id="navLinks">
<a class="active" href="/">Home</a>
<a href="/services.html">Services</a>
<a href="/service-area.html">Service Area</a>
<a href="/contact.html">Contact</a>
<a href="tel:14054106402" class="phone-link"><i class="fas fa-phone"></i> (405) 410-6402</a>
</nav>
<button class="mobile-menu-btn" id="mobileMenuBtn">
<i class="fas fa-bars"></i>
</button>
</div>
</header>

<!-- Breadcrumb -->
<div class="breadcrumb">
<div class="breadcrumb-container">
<a href="/">Home</a>
<i class="fas fa-chevron-right"></i>
<a href="/services.html">Services</a>
<i class="fas fa-chevron-right"></i>
<span>Accessibility Safety Solutions</span>
</div>
</div>

<main>
<section class="hero">
<div class="hero-content">
<h1>Accessibility Safety Solutions</h1>
<p>Expert ADA compliance and accessibility solutions in Norfolk, NE. We create safe, accessible environments for individuals with mobility challenges through professional modifications and installations.</p>
<div class="hero-cta">
<a href="/contact.html" class="cta-primary">Get Free Assessment</a>
<a href="tel:14054106402" class="cta-secondary">Call (405) 410-6402</a>
</div>
</div>
</section>

<section class="service-showcase">
<div class="container">
<h3>Comprehensive Accessibility Solutions</h3>
<div class="service-categories">
<div class="service-category">
<div class="category-icon">
<i class="fas fa-wheelchair"></i>
</div>
<div class="category-content">
<h4>ADA Compliant Modifications</h4>
<p>Professional installation of ADA-compliant ramps, grab bars, and bathroom modifications that meet all regulatory requirements.</p>
</div>
</div>
<div class="service-category">
<div class="category-icon">
<i class="fas fa-home"></i>
</div>
<div class="category-content">
<h4>Home Safety Assessments</h4>
<p>Comprehensive home evaluations to identify potential hazards and recommend safety improvements for aging in place.</p>
</div>
</div>
<div class="service-category">
<div class="category-icon">
<i class="fas fa-shower"></i>
</div>
<div class="category-content">
<h4>Bathroom Accessibility</h4>
<p>Zero-step showers, walk-in tubs, and accessible bathroom fixtures for safe and independent daily living.</p>
</div>
</div>
<div class="service-category">
<div class="category-icon">
<i class="fas fa-universal-access"></i>
</div>
<div class="category-content">
<h4>Mobility Solutions</h4>
<p>Custom ramps, stairlifts, and mobility aids to improve accessibility throughout your home or business.</p>
</div>
</div>
</div>
</div>
</section>

<section class="trust-section">
<div class="container">
<div class="trust-items">
<div class="trust-item">
<div class="trust-icon">
<i class="fas fa-certificate"></i>
</div>
<div class="trust-text">
<h5>ADA Compliant</h5>
<p>All modifications meet or exceed ADA standards</p>
</div>
</div>
<div class="trust-item">
<div class="trust-icon">
<i class="fas fa-award"></i>
</div>
<div class="trust-text">
<h5>Certified Professionals</h5>
<p>Licensed and insured accessibility specialists</p>
</div>
</div>
<div class="trust-item">
<div class="trust-icon">
<i class="fas fa-shield-alt"></i>
</div>
<div class="trust-text">
<h5>Safety First</h5>
<p>Prioritizing your safety and independence</p>
</div>
</div>
</div>
</div>
</section>

<section class="qa-section">
<div class="container">
<h2>Frequently Asked Questions</h2>
<div class="qa-cards">
<div class="qa-card">
<div class="qa-icon">
<i class="fas fa-question"></i>
</div>
<div class="qa-content">
<h3 class="qa-question">What is ADA compliance?</h3>
<p class="qa-answer">ADA compliance ensures that buildings and facilities are accessible to people with disabilities, following the Americans with Disabilities Act standards.</p>
</div>
</div>
<div class="qa-card">
<div class="qa-icon">
<i class="fas fa-question"></i>
</div>
<div class="qa-content">
<h3 class="qa-question">How long does installation take?</h3>
<p class="qa-answer">Most accessibility modifications can be completed in 1-3 days, depending on the scope of the project.</p>
</div>
</div>
<div class="qa-card">
<div class="qa-icon">
<i class="fas fa-question"></i>
</div>
<div class="qa-content">
<h3 class="qa-question">Do you work with insurance?</h3>
<p class="qa-answer">Yes, we work with various insurance providers and can help you navigate coverage options for accessibility modifications.</p>
</div>
</div>
</div>
</div>
</section>
</main>

<footer>
<div class="footer-container">
<div class="footer-section">
<h3>Watts Safety Installs</h3>
<p>Professional ADA accessibility contractor serving Norfolk, NE and surrounding areas.</p>
<div class="contact-info">
<p><i class="fas fa-phone"></i> (405) 410-6402</p>
<p><i class="fas fa-envelope"></i> wattssafetyinstalls@gmail.com</p>
<p><i class="fas fa-map-marker-alt"></i> Norfolk, NE</p>
</div>
</div>
<div class="footer-section">
<h3>Services</h3>
<ul>
<li><a href="/services/ada-compliant-showers/">ADA Showers</a></li>
<li><a href="/services/grab-bars/">Grab Bars</a></li>
<li><a href="/services/custom-ramps/">Wheelchair Ramps</a></li>
<li><a href="/services/senior-safety/">Senior Safety</a></li>
</ul>
</div>
<div class="footer-section">
<h3>Company</h3>
<ul>
<li><a href="/about.html">About Us</a></li>
<li><a href="/service-area.html">Service Area</a></li>
<li><a href="/contact.html">Contact</a></li>
<li><a href="/referrals.html">Referrals</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
<p>&copy; <span id="current-year">2024</span> Watts Safety Installs. All rights reserved.</p>
<div class="footer-links">
<a href="/privacy-policy.html">Privacy Policy</a>
<a href="/terms.html">Terms of Service</a>
</div>
</div>
</footer>

<script>
// Mobile menu toggle
document.getElementById('mobileMenuBtn').addEventListener('click', function() {
    document.getElementById('navLinks').classList.toggle('active');
});

// Update copyright year
document.getElementById('current-year').textContent = new Date().getFullYear();

// Q&A card interactions
document.querySelectorAll('.qa-card').forEach(card => {
    card.addEventListener('click', function() {
        this.classList.toggle('active');
    });
});
</script>

</body>
</html>'''
    
    # Combine head and body
    fixed_content = head_content + body_content
    
    # Write the fixed page
    accessibility_page.write_text(fixed_content, encoding='utf-8')
    logger.info("Fixed accessibility page - added missing body content")

if __name__ == "__main__":
    fix_accessibility_page()
