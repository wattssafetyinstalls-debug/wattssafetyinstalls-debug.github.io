import os

def fix_service_pages():
    services_dir = 'services'
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.html') and not filename.endswith('.backup'):
            filepath = os.path.join(services_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the CSS for touch devices
            old_css = """/* === TOUCH OPTIMIZATIONS === */
@media (hover: none) {
    .service-card:hover {
        transform: none;
    }
    
    .service-card:hover::before {
        left: -100%;
    }
    
    .service-card:hover .service-image {
        transform: none;
    }
    
    .service-card:hover .service-title {
        color: var(--navy);
    }
    
    .service-card:hover .service-description {
        color: var(--gray);
    }
    
    .service-dropdown {
        max-height: 0;
        padding: 0;
    }
    
    /* Add touch-friendly dropdown toggle */
    .service-card.touch-active .service-dropdown {
        max-height: 600px;
        padding: 25px;
    }
    
    .service-card.touch-active::before {
        left: 0;
    }
    
    .service-card.touch-active {
        transform: translateY(-12px);
        box-shadow: 0 25px 60px rgba(0,0,0,0.18);
    }
    
    .service-card.touch-active .service-title {
        color: white;
    }
    
    .service-card.touch-active .service-description {
        color: rgba(255,255,255,0.95);
    }
    
    .service-card.touch-active .service-image {
        transform: scale(1.05);
    }
}"""
            
            new_css = """/* === TOUCH OPTIMIZATIONS === */
@media (hover: none) {
    .service-card {
        cursor: pointer;
        transition: all 0.4s ease;
    }
    
    .service-card:hover {
        transform: none;
    }
    
    .service-card:hover::before {
        left: -100%;
    }
    
    .service-card:hover .service-image {
        transform: none;
    }
    
    .service-card:hover .service-title {
        color: var(--navy);
    }
    
    .service-card:hover .service-description {
        color: var(--gray);
    }
    
    .service-dropdown {
        max-height: 0;
        padding: 0;
        transition: max-height 0.4s ease, padding 0.4s ease;
    }
    
    /* Add touch-friendly dropdown toggle */
    .service-card.touch-active .service-dropdown {
        max-height: 600px;
        padding: 25px;
    }
    
    .service-card.touch-active::before {
        left: 0;
    }
    
    .service-card.touch-active {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .service-card.touch-active .service-title {
        color: white;
    }
    
    .service-card.touch-active .service-description {
        color: rgba(255,255,255,0.95);
    }
    
    .service-card.touch-active .service-image {
        transform: scale(1.05);
    }
}"""
            
            # Fix the JavaScript
            old_js = """// Touch-friendly service card interactions
if (window.matchMedia("(hover: none)").matches) {
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            // Close other open cards
            serviceCards.forEach(otherCard => {
                if (otherCard !== this && otherCard.classList.contains('touch-active')) {
                    otherCard.classList.remove('touch-active');
                }
            });
            
            // Toggle this card
            this.classList.toggle('touch-active');
        });
    });
    
    // Close service cards when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.service-card')) {
            serviceCards.forEach(card => {
                card.classList.remove('touch-active');
            });
        }
    });
}"""
            
            new_js = """// Touch-friendly service card interactions
if (window.matchMedia("(hover: none)").matches) {
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking a link inside the dropdown
            if (e.target.tagName === 'A') return;
            
            // Close other open cards
            serviceCards.forEach(otherCard => {
                if (otherCard !== this && otherCard.classList.contains('touch-active')) {
                    otherCard.classList.remove('touch-active');
                }
            });
            
            // Toggle this card
            this.classList.toggle('touch-active');
        });
    });
    
    // Close service cards when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.service-card')) {
            serviceCards.forEach(card => {
                card.classList.remove('touch-active');
            });
        }
    });
}"""
            
            # Replace the content
            content = content.replace(old_css, new_css)
            content = content.replace(old_js, new_js)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed: {filename}")

if __name__ == "__main__":
    fix_service_pages()
    print("Mobile tile fix applied to all service pages!")