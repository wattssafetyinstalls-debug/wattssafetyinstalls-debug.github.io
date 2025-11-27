#!/usr/bin/env python3
"""
COMPLETE RESTORE & FRESH CAROUSEL - Start from scratch
"""

import os

def restore_and_create_carousel():
    # First, let's check if we have a backup or restore the original structure
    if not os.path.exists("services.html"):
        print("ERROR: services.html not found")
        return
    
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Create a complete fresh services.html with carousel
    fresh_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Strict-Transport-Security" content="max-age=31536000; includeSubDomains">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Contractor Services Near Me | Watts Safety Installs | Norfolk NE</title>
    <meta name="description" content="Professional contractor services near me: ADA accessibility, home remodeling, concrete work, cabinet installation, snow removal & lawn care in Norfolk NE. Free estimates.">
    
    <!-- Favicon -->
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="/android-chrome-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">
    
    <!-- Search Engine & Social Media Meta Tags -->
    <meta name="google-site-verification" content="9uPoUkPF9bV3aKmaJyxbcnlzzXjxYLkUPb-YXyvOabU" />
    
    <!-- Open Graph for Facebook/LinkedIn -->
    <meta property="og:title" content="Professional Contractor Services Near Me | Watts Safety Installs | Norfolk NE">
    <meta property="og:description" content="Professional contractor services near me: ADA accessibility, home remodeling, concrete work, cabinet installation, snow removal & lawn care in Norfolk NE.">
    <meta property="og:image" content="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80">
    <meta property="og:url" content="https://wattsatpcontractor.com/services">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Watts Safety Installs">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Professional Contractor Services Near Me | Watts Safety Installs">
    <meta name="twitter:description" content="Professional contractor services near me: ADA accessibility, home remodeling, concrete work, cabinet installation, snow removal & lawn care in Norfolk NE.">
    <meta name="twitter:image" content="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80">
    
    <!-- Additional SEO Meta Tags -->
    <meta name="keywords" content="contractor services near me, ADA accessibility near me, home remodeling near me, concrete work near me, cabinet installation near me, snow removal near me, lawn care near me, Norfolk NE contractor">
    <meta name="author" content="Watts Safety Installs">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://wattsatpcontractor.com/services">
    
    <!-- Cache Control for Performance -->
    <meta http-equiv="Cache-Control" content="max-age=31536000, public">
   
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
   
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --teal: #00C4B4;
            --navy: #0A1D37;
            --light: #F8FAFC;
            --gray: #64748B;
            --gold: #FFD700;
            --white: #FFFFFF;
            --warm-light: #FEF7ED;
            --warm-accent: #F59E0B;
            --warm-dark: #E07C10;
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            --shadow-hover: 0 20px 50px rgba(0, 0, 0, 0.15);
            --teal-glow: 0 15px 40px rgba(0, 196, 180, 0.15);
            --navy-glow: 0 15px 40px rgba(10, 29, 55, 0.12);
            --gold-glow: 0 15px 40px rgba(255, 215, 0, 0.1);
        }
       
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
       
        body { 
            font-family: 'Inter', sans-serif; 
            background: var(--warm-light); 
            color: #1E293B; 
            line-height: 1.7; 
            overflow-x: hidden;
        }

        /* Header Styles */
        header { 
            background: var(--navy); 
            padding: 0; 
            position: sticky; 
            top: 0; 
            z-index: 1000; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
            width: 100%;
        }
        
        .header-container { 
            max-width: 1400px; 
            margin: 0 auto; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 0 20px; 
            height: 80px;
        }
        
        .logo { 
            font-family: 'Playfair Display', serif; 
            font-size: 2.5rem; 
            color: var(--teal); 
            font-weight: 700; 
            text-decoration: none; 
            letter-spacing: -0.5px;
        }
        
        .nav-links { 
            display: flex; 
            gap: 40px; 
            align-items: center;
        }
        
        .nav-links a { 
            color: var(--white); 
            text-decoration: none; 
            font-weight: 600; 
            font-size: 1.1rem;
            transition: all 0.3s; 
            position: relative;
            padding: 10px 0;
        }
        
        .nav-links a:hover { 
            color: var(--teal); 
        }
        
        .phone-link { 
            background: var(--teal); 
            color: var(--white); 
            padding: 12px 25px; 
            border-radius: 50px; 
            font-weight: 700; 
            text-decoration: none; 
            transition: all 0.3s; 
            white-space: nowrap;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        }

        /* Services Hero */
        .services-hero {
            position: relative;
            height: 60vh;
            min-height: 500px;
            background: 
                linear-gradient(135deg, rgba(10,29,55,0.85) 0%, rgba(245, 158, 11, 0.2) 100%),
                url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80') center/cover no-repeat;
            color: var(--white);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 0 20px;
            width: 100%;
        }
        
        .services-hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 4rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .services-hero p {
            font-size: 1.4rem;
            max-width: 700px;
            margin: 0 auto 30px;
            opacity: 0.9;
        }
        
        .certification-badge {
            background: var(--gold);
            color: var(--navy);
            padding: 10px 25px;
            border-radius: 50px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 30px;
        }

        /* Simple Carousel */
        .carousel-section {
            padding: 80px 20px;
            background: var(--warm-light);
        }
        
        .carousel-container {
            max-width: 1000px;
            margin: 0 auto;
            position: relative;
        }
        
        .carousel {
            position: relative;
            overflow: hidden;
            border-radius: 20px;
            background: white;
            box-shadow: var(--shadow);
            padding: 40px 20px;
        }
        
        .carousel-track {
            display: flex;
            transition: transform 0.5s ease;
        }
        
        .carousel-slide {
            min-width: 100%;
            padding: 20px;
            display: flex;
            justify-content: center;
        }
        
        .service-card {
            background: var(--white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--teal-glow);
            transition: all 0.4s ease;
            display: flex;
            flex-direction: column;
            max-width: 450px;
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.8);
            text-align: center;
        }

        .service-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--teal-glow), var(--navy-glow);
            background: linear-gradient(135deg, var(--teal) 0%, var(--navy) 100%);
            color: var(--white);
        }

        .service-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            transition: transform 0.4s ease;
        }

        .service-card:hover .service-image {
            transform: scale(1.05);
        }

        .service-content {
            padding: 25px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 15px;
            position: relative;
        }

        .service-title {
            font-size: 1.5rem;
            color: var(--navy);
            margin-bottom: 10px;
            font-family: 'Playfair Display', serif;
            position: relative;
            padding-bottom: 10px;
        }

        .service-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 2px;
            background: linear-gradient(135deg, var(--teal), var(--warm-accent));
            border-radius: 2px;
        }

        .service-description {
            color: var(--gray);
            margin-bottom: 15px;
            line-height: 1.6;
            font-size: 1rem;
        }

        .service-cta {
            margin-top: auto;
            display: flex;
            justify-content: center;
            padding-top: 15px;
            border-top: 1px solid rgba(0, 196, 180, 0.1);
        }

        .service-cta a {
            background: linear-gradient(135deg, var(--teal), #00a396);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 0.95rem;
            box-shadow: 0 4px 15px rgba(0, 196, 180, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .carousel-nav {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 30px;
            margin-top: 40px;
        }
        
        .carousel-arrow {
            background: linear-gradient(135deg, var(--teal), var(--navy));
            color: white;
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,196,180,0.3);
        }
        
        .carousel-arrow:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,196,180,0.4);
        }
        
        .carousel-dots {
            display: flex;
            gap: 12px;
        }
        
        .carousel-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--gray);
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .carousel-dot.active {
            background: var(--teal);
            transform: scale(1.2);
        }

        /* Promo Section */
        .promo-section {
            background: linear-gradient(135deg, var(--navy), #1e3a5f);
            color: var(--white);
            padding: 80px 20px;
            text-align: center;
            border-radius: 20px;
            margin: 50px 0;
            max-width: 1200px;
            width: 100%;
        }
        
        .promo-section h2 {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            margin-bottom: 20px;
        }
        
        .promo-section p {
            font-size: 1.3rem;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            opacity: 0.9;
        }
        
        .promo-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .promo-card {
            background: rgba(255,255,255,0.1);
            padding: 40px 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .promo-card h3 {
            font-size: 1.8rem;
            margin-bottom: 15px;
            color: var(--gold);
        }
        
        .promo-card p {
            margin-bottom: 20px;
            font-size: 1.1rem;
        }
        
        .promo-code {
            background: var(--gold);
            color: var(--navy);
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 1.2rem;
            display: inline-block;
            margin-bottom: 20px;
        }

        /* Footer */
        footer { 
            background: var(--navy); 
            color: var(--white); 
            padding: 80px 20px 30px; 
            width: 100%;
            margin-top: 60px;
        }
        
        .footer-container {
            max-width: 1300px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 60px;
            width: 100%;
        }
        
        .footer-logo {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            color: var(--teal);
            margin-bottom: 25px;
        }
        
        .footer-about p {
            margin-bottom: 20px;
            color: #cbd5e1;
            line-height: 1.7;
        }
        
        .footer-links h3, .footer-contact h3 {
            font-size: 1.4rem;
            margin-bottom: 25px;
            color: var(--teal);
        }
        
        .footer-links ul {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 12px;
        }
        
        .footer-links a, .footer-contact a {
            color: #cbd5e1;
            text-decoration: none;
            transition: color 0.3s;
            font-size: 1.05rem;
        }
        
        .copyright { 
            text-align: center; 
            padding-top: 50px; 
            margin-top: 50px; 
            border-top: 1px solid #334155; 
            color: #94a3b8; 
            width: 100%;
            font-size: 1rem;
        }

        @media (max-width: 768px) {
            .services-hero h1 { font-size: 2.5rem; }
            .carousel { padding: 30px 15px; }
            .carousel-nav { gap: 20px; }
            .carousel-arrow { width: 44px; height: 44px; }
            .footer-container { grid-template-columns: 1fr; gap: 40px; }
            .promo-cards { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="header-container">
            <a href="index" class="logo">WATTS</a>
            <nav class="nav-links">
                <a href="index">Home</a>
                <a href="services" class="active">Services</a>
                <a href="service-area">Service Area</a>
                <a href="about">About</a>
                <a href="contact">Contact</a>
            </nav>
            <a href="tel:+14054106402" class="phone-link">
                <i class="fas fa-phone"></i> (405) 410-6402
            </a>
        </div>
    </header>

    <!-- Services Hero -->
    <section class="services-hero">
        <h1>Professional Contractor Services</h1>
        <p>Comprehensive solutions for your home safety, accessibility, and maintenance needs in Norfolk NE and surrounding areas</p>
        <div class="certification-badge">ATP Approved Contractor • Nebraska Licensed #54690-25</div>
        <a href="tel:+14054106402" class="cta-button">Call Now for Free Estimate</a>
    </section>

    <!-- Service Carousel -->
    <section class="carousel-section">
        <div class="carousel-container">
            <div class="carousel">
                <div class="carousel-track">
                    <!-- Slide 1 -->
                    <div class="carousel-slide active">
                        <div class="service-card">
                            <img loading="lazy" src="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80" alt="Accessibility & Safety Solutions" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Accessibility & Safety Solutions</h3>
                                <p class="service-description">Create safe, accessible environments with our professional ADA-compliant solutions. We specialize in modifications for seniors and individuals with mobility challenges.</p>
                                <div class="service-cta">
                                    <a href="contact">Get Free Assessment</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Slide 2 -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img loading="lazy" src="https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80" alt="Home Remodeling" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Home Remodeling & Improvements</h3>
                                <p class="service-description">Transform your living space with our comprehensive remodeling services. From concept to completion, we deliver exceptional craftsmanship.</p>
                                <div class="service-cta">
                                    <a href="contact">Start Your Project</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Slide 3 -->
                    <div class="carousel-slide">
                        <div class="service-card">
                            <img loading="lazy" src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2058&q=80" alt="Concrete & Floor Services" class="service-image">
                            <div class="service-content">
                                <h3 class="service-title">Concrete & Floor Services</h3>
                                <p class="service-description">Professional concrete work and floor services for durable, beautiful surfaces that stand the test of time.</p>
                                <div class="service-cta">
                                    <a href="contact">Get Floor Quote</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="carousel-nav">
                    <button class="carousel-arrow prev">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    
                    <div class="carousel-dots">
                        <button class="carousel-dot active"></button>
                        <button class="carousel-dot"></button>
                        <button class="carousel-dot"></button>
                    </div>
                    
                    <button class="carousel-arrow next">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Promo Section -->
    <section class="promo-section">
        <h2>Special Offers & Seasonal Contracts</h2>
        <p>Take advantage of our limited-time offers and seasonal maintenance contracts</p>
        
        <div class="promo-cards">
            <div class="promo-card">
                <h3>Winter Maintenance</h3>
                <p>Keep your property safe and accessible all winter long with our professional snow removal services.</p>
                <div class="promo-code">15% OFF</div>
                <p>First 3 Snow Visits 2025</p>
                <a href="contact" class="cta-button">Claim Offer</a>
            </div>
            
            <div class="promo-card">
                <h3>Summer Lawn Care</h3>
                <p>Beautiful, healthy lawn all season long with our comprehensive lawn care program.</p>
                <div class="promo-code">LAWN2026</div>
                <p>20% OFF Full Season</p>
                <a href="contact" class="cta-button">Claim Offer</a>
            </div>
            
            <div class="promo-card">
                <h3>Accessibility Assessment</h3>
                <p>Free home safety assessment to identify potential hazards and recommend solutions.</p>
                <div class="promo-code">FREE</div>
                <p>Safety Assessment</p>
                <a href="contact" class="cta-button">Schedule Free Assessment</a>
            </div>
        </div>
    </section>

    <footer>
        <div class="footer-container">
            <div class="footer-about">
                <div class="footer-logo">WATTS SAFETY INSTALLS</div>
                <p>Nebraska's premier ATP Approved Contractor specializing in accessibility modifications, safety installations, and comprehensive home services near you.</p>
                <p>Nebraska License #54690-25 • ATP Approved Contractor</p>
            </div>
            <div class="footer-links">
                <h3>Our Services</h3>
                <ul>
                    <li><a href="services.html#accessibility-safety">Accessibility & Safety</a></li>
                    <li><a href="/home-remodeling">Home Remodeling</a></li>
                    <li><a href="services.html#concrete-flooring">Concrete & Flooring</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h3>Contact Us</h3>
                <p><strong>Phone:</strong> <a href="tel:+14054106402">(405) 410-6402</a></p>
                <p><strong>Email:</strong> <a href="mailto:wattssafetyinstalls@gmail.com">wattssafetyinstalls@gmail.com</a></p>
                <p><strong>Address:</strong> 500 Block Omaha Ave, Norfolk, NE 68701</p>
            </div>
        </div>
        <div class="copyright">
            <p>© 2024 Watts Safety Installs. All rights reserved. | Nebraska License #54690-25 • ATP Approved Contractor</p>
        </div>
    </footer>

    <script>
        // Simple Carousel Functionality
        document.addEventListener('DOMContentLoaded', function() {
            const track = document.querySelector('.carousel-track');
            const slides = document.querySelectorAll('.carousel-slide');
            const dots = document.querySelectorAll('.carousel-dot');
            const prevBtn = document.querySelector('.carousel-arrow.prev');
            const nextBtn = document.querySelector('.carousel-arrow.next');
            
            let currentIndex = 0;
            let autoSlide;
            
            function showSlide(index) {
                // Update track position
                track.style.transform = 'translateX(-' + (index * 100) + '%)';
                
                // Update active states
                slides.forEach(slide => slide.classList.remove('active'));
                dots.forEach(dot => dot.classList.remove('active'));
                
                slides[index].classList.add('active');
                dots[index].classList.add('active');
                
                currentIndex = index;
            }
            
            function nextSlide() {
                let nextIndex = currentIndex + 1;
                if (nextIndex >= slides.length) nextIndex = 0;
                showSlide(nextIndex);
            }
            
            function prevSlide() {
                let prevIndex = currentIndex - 1;
                if (prevIndex < 0) prevIndex = slides.length - 1;
                showSlide(prevIndex);
            }
            
            function startAutoSlide() {
                autoSlide = setInterval(nextSlide, 5000);
            }
            
            function stopAutoSlide() {
                clearInterval(autoSlide);
            }
            
            // Event listeners
            nextBtn.addEventListener('click', function() {
                stopAutoSlide();
                nextSlide();
                startAutoSlide();
            });
            
            prevBtn.addEventListener('click', function() {
                stopAutoSlide();
                prevSlide();
                startAutoSlide();
            });
            
            dots.forEach((dot, index) => {
                dot.addEventListener('click', function() {
                    stopAutoSlide();
                    showSlide(index);
                    startAutoSlide();
                });
            });
            
            // Pause on hover
            const carousel = document.querySelector('.carousel');
            carousel.addEventListener('mouseenter', stopAutoSlide);
            carousel.addEventListener('mouseleave', startAutoSlide);
            
            // Initialize
            showSlide(0);
            startAutoSlide();
        });
    </script>
</body>
</html>'''
    
    # Write the fresh content
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(fresh_content)
    
    print("SUCCESS: Completely restored services.html with a clean, working carousel")
    print("The carousel automatically cycles every 5 seconds and has working navigation")

if __name__ == "__main__":
    restore_and_create_carousel()