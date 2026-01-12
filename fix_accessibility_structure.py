#!/usr/bin/env python3
"""
Fix Accessibility Page Structure
Make it match the exact structure of other service pages with Q&A carousel
"""

import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_accessibility_page_structure():
    """Fix the accessibility page to match the exact structure of other service pages"""
    
    base_dir = Path(r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec")
    accessibility_page = base_dir / "services" / "accessibility-safety-solutions" / "index.html"
    
    # Read the senior-safety page as a template
    template_page = base_dir / "services" / "senior-safety" / "index.html"
    
    if not template_page.exists():
        logger.error("Template page not found")
        return
    
    template_content = template_page.read_text(encoding='utf-8', errors='ignore')
    
    # Create accessibility-specific content by replacing senior-safety content
    accessibility_content = template_content
    
    # Replace title and meta tags
    accessibility_content = accessibility_content.replace(
        '<title>Senior Safety | Watts At Your Service</title>',
        '<title>Accessibility Safety Solutions | Watts Safety Installs</title>'
    )
    
    accessibility_content = accessibility_content.replace(
        '<meta content="Comprehensive senior safety modifications in Norfolk, NE. We assess homes for fall risks and implement proven safety solutions including grab bars, ramps, and bathroom accessibility upgrades." name="description"/>',
        '<meta content="Expert ADA compliance and accessibility solutions in Norfolk, NE. We create safe, accessible environments for individuals with mobility challenges through professional modifications and installations." name="description"/>'
    )
    
    accessibility_content = accessibility_content.replace(
        '<link href="https://wattsatpcontractor.com/services/senior-safety" rel="canonical"/>',
        '<link href="https://wattsatpcontractor.com/services/accessibility-safety-solutions/" rel="canonical"/>'
    )
    
    # Replace hero section
    accessibility_content = accessibility_content.replace(
        '<h1 class="service-title">Senior Safety</h1>',
        '<h1 class="service-title">Accessibility Safety Solutions</h1>'
    )
    
    accessibility_content = accessibility_content.replace(
        '<p><strong>Professional senior safety services in Norfolk, NE.</strong> Comprehensive senior safety modifications in Norfolk, NE. We assess homes for fall risks and implement proven safety solutions including grab bars, ramps, and bathroom accessibility upgrades.</p>',
        '<p><strong>Professional accessibility solutions in Norfolk, NE.</strong> Expert ADA compliance and accessibility modifications in Norfolk, NE. We create safe, accessible environments for individuals with mobility challenges through professional installations of ramps, grab bars, and bathroom modifications.</p>'
    )
    
    accessibility_content = accessibility_content.replace(
        '<p>Professional Senior Safety in Norfolk, NE</p>',
        '<p>Professional Accessibility Solutions in Norfolk, NE</p>'
    )
    
    # Replace service categories section
    old_services = '''<section class="service-categories">
<div class="container">
<h2>Our Senior Safety Services</h2>
<div class="services-grid">
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-home"></i>
</div>
<div class="tile-content">
<h3>Fall Risk Assessment</h3>
<p>Comprehensive home safety evaluations to identify and eliminate fall hazards for seniors.</p>
</div>
</div>
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-shower"></i>
</div>
<div class="tile-content">
<h3>Bathroom Safety</h3>
<p>Grab bars, walk-in tubs, and accessible bathroom modifications for senior safety.</p>
</div>
</div>
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-universal-access"></i>
</div>
<div class="tile-content">
<h3>Mobility Solutions</h3>
<p>Ramps, stairlifts, and mobility aids to improve accessibility and independence.</p>
</div>
</div>
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-bed"></i>
</div>
<div class="tile-content">
<h3>Bedroom Safety</h3>
<p>Bed rails, accessible furniture, and bedroom modifications for senior comfort.</p>
</div>
</div>
</div>
</div>
</section>'''
    
    new_services = '''<section class="service-categories">
<div class="container">
<h2>Our Accessibility Solutions</h2>
<div class="services-grid">
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-wheelchair"></i>
</div>
<div class="tile-content">
<h3>ADA Compliance</h3>
<p>Professional ADA-compliant modifications including ramps, grab bars, and accessible fixtures.</p>
</div>
</div>
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-shower"></i>
</div>
<div class="tile-content">
<h3>Bathroom Accessibility</h3>
<p>Zero-step showers, walk-in tubs, and accessible bathroom fixtures for independent living.</p>
</div>
</div>
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-home"></i>
</div>
<div class="tile-content">
<h3>Home Safety Assessments</h3>
<p>Comprehensive evaluations to identify hazards and recommend safety improvements.</p>
</div>
</div>
<div class="service-tile">
<div class="tile-icon">
<i class="fas fa-universal-access"></i>
</div>
<div class="tile-content">
<h3>Mobility Solutions</h3>
<p>Custom ramps, stairlifts, and modifications to improve accessibility throughout your home.</p>
</div>
</div>
</div>
</div>
</section>'''
    
    accessibility_content = accessibility_content.replace(old_services, new_services)
    
    # Replace Q&A section
    old_qa = '''<!-- Q&A CAROUSEL SECTION -->
<div class="container">
<section class="qa-section">
<h2>Senior Safety Questions &amp; Answers</h2>
<p class="section-subtitle">Real answers from local experts. Every project is different — get your custom quote today.</p>'''
    
    new_qa = '''<!-- Q&A CAROUSEL SECTION -->
<div class="container">
<section class="qa-section">
<h2>Accessibility Safety Solutions Questions &amp; Answers</h2>
<p class="section-subtitle">Real answers from local experts. Every project is different — get your custom quote today.</p>'''
    
    accessibility_content = accessibility_content.replace(old_qa, new_qa)
    
    # Replace Q&A cards content
    old_qa_cards = '''<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">What modifications do you recommend for senior safety?</h3>
<p class="qa-answer">We recommend grab bars in bathrooms, non-slip flooring, improved lighting, and removing tripping hazards. Each home is assessed individually.</p>
</div>
</div>
<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">How long does installation take?</h3>
<p class="qa-answer">Most installations take 1-3 days depending on the scope. We work efficiently to minimize disruption to your daily routine.</p>
</div>
</div>
<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">Do you work with Medicare or insurance?</h3>
<p class="qa-answer">We can provide documentation for insurance claims and work with healthcare providers. Coverage varies by plan.</p>
</div>
</div>
<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">Are your modifications ADA compliant?</h3>
<p class="qa-answer">Yes, all our modifications meet or exceed ADA requirements. We're licensed and insured for your protection.</p>
</div>
</div>'''
    
    new_qa_cards = '''<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">What is ADA compliance?</h3>
<p class="qa-answer">ADA compliance ensures buildings and facilities are accessible to people with disabilities, following the Americans with Disabilities Act standards.</p>
</div>
</div>
<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">How long does installation take?</h3>
<p class="qa-answer">Most accessibility modifications can be completed in 1-3 days, depending on the scope of the project.</p>
</div>
</div>
<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">Do you work with insurance?</h3>
<p class="qa-answer">Yes, we work with various insurance providers and can help you navigate coverage options for accessibility modifications.</p>
</div>
</div>
<div class="qa-card">
<i class="fas fa-lightbulb qa-icon"></i>
<div class="qa-content">
<h3 class="qa-question">Are you licensed and insured?</h3>
<p class="qa-answer">Yes, we're fully licensed, insured, and ATP approved contractors with extensive experience in accessibility modifications.</p>
</div>
</div>'''
    
    accessibility_content = accessibility_content.replace(old_qa_cards, new_qa_cards)
    
    # Update JSON-LD structured data
    old_json = '''"mainEntity": [
    {
      "@type": "Question",
      "name": "What modifications do you recommend for senior safety?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We recommend grab bars in bathrooms, non-slip flooring, improved lighting, and removing tripping hazards. Each home is assessed individually."
      }
    },
    {
      "@type": "Question",
      "name": "How long does installation take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most installations take 1-3 days depending on the scope. We work efficiently to minimize disruption to your daily routine."
      }
    },
    {
      "@type": "Question",
      "name": "Do you work with Medicare or insurance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We can provide documentation for insurance claims and work with healthcare providers. Coverage varies by plan."
      }
    },
    {
      "@type": "Question",
      "name": "Are your modifications ADA compliant?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, all our modifications meet or exceed ADA requirements. We're licensed and insured for your protection."
      }
    }'''
    
    new_json = '''"mainEntity": [
    {
      "@type": "Question",
      "name": "What is ADA compliance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ADA compliance ensures that buildings and facilities are accessible to people with disabilities, following the Americans with Disabilities Act standards."
      }
    },
    {
      "@type": "Question",
      "name": "How long does installation take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most accessibility modifications can be completed in 1-3 days, depending on the scope of the project."
      }
    },
    {
      "@type": "Question",
      "name": "Do you work with insurance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, we work with various insurance providers and can help you navigate coverage options for accessibility modifications."
      }
    },
    {
      "@type": "Question",
      "name": "Are you licensed and insured?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, we're fully licensed, insured, and ATP approved contractors with extensive experience in accessibility modifications."
      }
    }'''
    
    accessibility_content = accessibility_content.replace(old_json, new_json)
    
    # Write the fixed page
    accessibility_page.write_text(accessibility_content, encoding='utf-8')
    logger.info("Fixed accessibility page structure to match other service pages")

if __name__ == "__main__":
    fix_accessibility_page_structure()
