"""
جایگزین کن با فایل:
products/management/commands/seed_data.py

قبلش حتما همه Product و Category های قبلی (فارسی و ناقص) رو از Admin پاک کن.

سپس اجرا کن:
python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product, ProductSize


class Command(BaseCommand):
    help = 'پر کردن دیتابیس با دسته‌بندی و محصولات نمونه (10 محصول در هر برند)'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seed...")

        categories_data = [
            {'name': 'Nike', 'slug': 'nike', 'description': 'Premium athletic footwear with cutting-edge innovation and iconic style.'},
            {'name': 'Adidas', 'slug': 'adidas', 'description': 'Performance-driven sneakers combining comfort, quality, and street style.'},
            {'name': 'Balenciaga', 'slug': 'balenciaga', 'description': 'Luxury high-fashion sneakers with bold, avant-garde design.'},
            {'name': 'Puma', 'slug': 'puma', 'description': 'Sporty and casual shoes built for speed, comfort, and everyday style.'},
            {'name': 'New Balance', 'slug': 'new-balance', 'description': 'Classic comfort meets modern design in every pair.'},
            {'name': 'Converse', 'slug': 'converse', 'description': 'Timeless canvas sneakers loved across generations.'},
            {'name': 'Vans', 'slug': 'vans', 'description': 'Skate-inspired shoes with a laid-back, iconic look.'},
            {'name': 'Jordan', 'slug': 'jordan', 'description': 'Legendary basketball-inspired sneakers with unmatched street cred.'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                }
            )
            categories[cat_data['name']] = category
            status = "created" if created else "exists"
            self.stdout.write(f"  [{status}] Category: {cat_data['name']}")

        # ===== هر برند دقیقا 10 محصول =====
        products_data = {
            'Nike': [
                {'name': 'Nike Air Max 270', 'description': 'A sleek, versatile sneaker featuring Nike\'s largest heel Air unit yet, delivering all-day comfort with a bold, modern silhouette.', 'price': 4500000, 'discount_price': 3800000, 'stock': 25},
                {'name': 'Nike Air Force 1', 'description': 'The timeless icon. Crisp leather upper, classic silhouette, and unbeatable comfort — a street style essential since day one.', 'price': 3800000, 'discount_price': None, 'stock': 30},
                {'name': 'Nike Zoom Pegasus 40', 'description': 'A responsive daily trainer built for runners of every level, combining lightweight cushioning with a breathable, secure fit.', 'price': 5200000, 'discount_price': 4600000, 'stock': 18},
                {'name': 'Nike Blazer Mid 77', 'description': 'A retro-inspired basketball sneaker with vintage detailing and a padded collar for effortless off-court style.', 'price': 3500000, 'discount_price': None, 'stock': 22},
                {'name': 'Nike React Infinity', 'description': 'Engineered to help reduce injury and keep you running, featuring plush React foam for a smooth, stable ride.', 'price': 4800000, 'discount_price': 4200000, 'stock': 15},
                {'name': 'Nike Dunk Low', 'description': 'A basketball classic reborn, featuring crisp color-blocking and a low-cut silhouette perfect for everyday wear.', 'price': 4200000, 'discount_price': None, 'stock': 20},
                {'name': 'Nike Air Max 90', 'description': 'A 90s icon reborn, featuring visible Air cushioning and classic layered mesh and leather construction.', 'price': 4400000, 'discount_price': None, 'stock': 19},
                {'name': 'Nike Cortez', 'description': 'A running heritage icon with a slim silhouette and timeless two-tone design.', 'price': 3300000, 'discount_price': 2900000, 'stock': 23},
                {'name': 'Nike SB Dunk', 'description': 'A skate-ready version of the Dunk with extra padding and grippy outsole for board feel.', 'price': 4600000, 'discount_price': None, 'stock': 16},
                {'name': 'Nike Air Max 97', 'description': 'Inspired by Japanese bullet trains, featuring full-length Air cushioning and a wavy, reflective design.', 'price': 5000000, 'discount_price': 4400000, 'stock': 17},
            ],
            'Adidas': [
                {'name': 'Adidas Ultraboost 22', 'description': 'Experience incredible energy return with responsive Boost cushioning and a sock-like Primeknit upper.', 'price': 5500000, 'discount_price': 4900000, 'stock': 20},
                {'name': 'Adidas Stan Smith', 'description': 'The definition of clean, minimalist style — a tennis-inspired classic that pairs with everything.', 'price': 3200000, 'discount_price': None, 'stock': 35},
                {'name': 'Adidas Gazelle', 'description': 'A retro icon from the 70s, featuring soft suede and a low-profile silhouette loved by sneakerheads worldwide.', 'price': 3400000, 'discount_price': 2900000, 'stock': 28},
                {'name': 'Adidas NMD R1', 'description': 'A futuristic streetwear staple combining Boost cushioning with a bold, sporty design.', 'price': 3900000, 'discount_price': None, 'stock': 24},
                {'name': 'Adidas Forum Low', 'description': 'Bold, chunky, and full of basketball heritage — the Forum brings retro flair to modern streetwear.', 'price': 4100000, 'discount_price': 3700000, 'stock': 19},
                {'name': 'Adidas Superstar', 'description': 'The iconic shell-toe sneaker that defined a generation of hip-hop and street culture.', 'price': 3300000, 'discount_price': None, 'stock': 26},
                {'name': 'Adidas Samba', 'description': 'A football-inspired classic turned streetwear favorite, known for its sleek suede overlays.', 'price': 3100000, 'discount_price': 2700000, 'stock': 30},
                {'name': 'Adidas Ozweego', 'description': 'A chunky dad-shoe silhouette with exaggerated proportions and cushioned comfort.', 'price': 3700000, 'discount_price': None, 'stock': 21},
                {'name': 'Adidas Yeezy Boost 350', 'description': 'A minimalist knit sneaker with signature Boost cushioning and a highly coveted silhouette.', 'price': 8900000, 'discount_price': 7900000, 'stock': 9},
                {'name': 'Adidas Campus 00s', 'description': 'A revived Y2K classic with a suede upper and low-profile silhouette, beloved by streetwear fans.', 'price': 3600000, 'discount_price': None, 'stock': 22},
            ],
            'Balenciaga': [
                {'name': 'Balenciaga Triple S', 'description': 'A statement-making chunky sneaker with layered soles, blending luxury craftsmanship with bold streetwear energy.', 'price': 18500000, 'discount_price': None, 'stock': 8},
                {'name': 'Balenciaga Speed Trainer', 'description': 'A sock-like knit sneaker offering second-skin comfort with a sleek, futuristic silhouette.', 'price': 16800000, 'discount_price': 14500000, 'stock': 6},
                {'name': 'Balenciaga Track', 'description': 'An intricate, multi-layered sneaker design that redefined luxury sportswear aesthetics.', 'price': 21000000, 'discount_price': None, 'stock': 5},
                {'name': 'Balenciaga Defender', 'description': 'A rugged, oversized sneaker built for maximum impact with a thick, sculpted sole.', 'price': 19200000, 'discount_price': 17000000, 'stock': 7},
                {'name': 'Balenciaga Runner', 'description': 'A destroyed-effect sneaker with a distressed knit upper for an avant-garde street look.', 'price': 17500000, 'discount_price': None, 'stock': 6},
                {'name': 'Balenciaga Track 2', 'description': 'An evolved version of the Track, with a more streamlined silhouette and dual-material build.', 'price': 20200000, 'discount_price': 18000000, 'stock': 5},
                {'name': 'Balenciaga Tyrex', 'description': 'A sock-style sneaker fusing sportswear comfort with high-fashion sensibility.', 'price': 15900000, 'discount_price': None, 'stock': 7},
                {'name': 'Balenciaga Cargo', 'description': 'A utilitarian-inspired sneaker with rugged detailing and heavy-duty construction.', 'price': 18900000, 'discount_price': None, 'stock': 6},
                {'name': 'Balenciaga 3XL', 'description': 'An extreme chunky silhouette pushing sneaker design to its most maximalist form.', 'price': 22500000, 'discount_price': 20000000, 'stock': 4},
                {'name': 'Balenciaga Rise', 'description': 'A sleek slip-on sneaker with a rocker sole for a bold, elongated silhouette.', 'price': 17800000, 'discount_price': None, 'stock': 5},
            ],
            'Puma': [
                {'name': 'Puma RS-X', 'description': 'A retro-futuristic runner with chunky proportions and plush cushioning for all-day comfort.', 'price': 3100000, 'discount_price': 2700000, 'stock': 26},
                {'name': 'Puma Suede Classic', 'description': 'A timeless streetwear icon crafted from soft suede — effortlessly cool since the 1960s.', 'price': 2600000, 'discount_price': None, 'stock': 32},
                {'name': 'Puma Cali', 'description': 'A sleek, sporty silhouette with a clean design inspired by California street style.', 'price': 2900000, 'discount_price': None, 'stock': 27},
                {'name': 'Puma Future Rider', 'description': 'A retro-inspired sneaker with playful color-blocking and lightweight foam cushioning.', 'price': 3300000, 'discount_price': 2900000, 'stock': 21},
                {'name': 'Puma Mayze', 'description': 'A platform sneaker built on a retro-runner base, offering extra height and street style.', 'price': 3400000, 'discount_price': None, 'stock': 20},
                {'name': 'Puma Slipstream', 'description': 'A basketball-inspired classic with clean lines and a low-top silhouette.', 'price': 3000000, 'discount_price': None, 'stock': 24},
                {'name': 'Puma Palermo', 'description': 'A vintage soccer-inspired sneaker with soft suede and a slim, retro profile.', 'price': 2800000, 'discount_price': 2400000, 'stock': 25},
                {'name': 'Puma Speedcat', 'description': 'A low-profile racing-inspired sneaker built for a sleek, aerodynamic look.', 'price': 2700000, 'discount_price': None, 'stock': 22},
                {'name': 'Puma Deviate Nitro', 'description': 'A performance running shoe with Nitro foam cushioning for responsive, lightweight speed.', 'price': 4900000, 'discount_price': 4300000, 'stock': 14},
                {'name': 'Puma Rider FV', 'description': 'A bold retro-runner with exaggerated proportions and a comfortable EVA midsole.', 'price': 3200000, 'discount_price': None, 'stock': 19},
            ],
            'New Balance': [
                {'name': 'New Balance 550', 'description': 'A retro basketball sneaker with premium leather panels and a clean, versatile look.', 'price': 4300000, 'discount_price': None, 'stock': 18},
                {'name': 'New Balance 990v5', 'description': 'Made in the USA with premium materials, delivering superior comfort and timeless style.', 'price': 6200000, 'discount_price': 5500000, 'stock': 12},
                {'name': 'New Balance 574', 'description': 'A classic runner silhouette offering ENCAP cushioning for a smooth, supportive ride.', 'price': 3600000, 'discount_price': None, 'stock': 24},
                {'name': 'New Balance 2002R', 'description': 'A retro-runner with a protective toe cap and plush ABZORB cushioning for all-day wear.', 'price': 4700000, 'discount_price': 4100000, 'stock': 16},
                {'name': 'New Balance 327', 'description': 'A bold silhouette drawing on 70s running heritage with an exaggerated N logo.', 'price': 3900000, 'discount_price': None, 'stock': 19},
                {'name': 'New Balance 1906R', 'description': 'A protection-focused runner with ABZORB cushioning for a smooth, cushioned stride.', 'price': 4800000, 'discount_price': None, 'stock': 15},
                {'name': 'New Balance 993', 'description': 'A premium made-in-USA classic offering superior stability and everyday comfort.', 'price': 6800000, 'discount_price': 6000000, 'stock': 10},
                {'name': 'New Balance 530', 'description': 'A retro-tech runner with a chunky silhouette and reflective detailing.', 'price': 3500000, 'discount_price': None, 'stock': 20},
                {'name': 'New Balance Fresh Foam 1080', 'description': 'A plush daily trainer with Fresh Foam midsole for ultra-soft, cushioned rides.', 'price': 5300000, 'discount_price': 4700000, 'stock': 13},
                {'name': 'New Balance 9060', 'description': 'A dad-shoe-inspired silhouette with layered mesh and suede for a bold retro-futuristic look.', 'price': 5100000, 'discount_price': None, 'stock': 14},
            ],
            'Converse': [
                {'name': 'Converse Chuck Taylor All Star', 'description': 'The original canvas sneaker — an enduring symbol of self-expression for over a century.', 'price': 2200000, 'discount_price': None, 'stock': 40},
                {'name': 'Converse Chuck 70', 'description': 'An elevated take on the classic Chuck, featuring premium materials and vintage detailing.', 'price': 2800000, 'discount_price': 2400000, 'stock': 22},
                {'name': 'Converse Run Star Hike', 'description': 'A platform sneaker built on rugged, elevated soles for a bold, modern twist on a classic.', 'price': 3400000, 'discount_price': None, 'stock': 18},
                {'name': 'Converse One Star', 'description': 'A retro skate-inspired silhouette featuring the iconic single-star branding.', 'price': 2600000, 'discount_price': None, 'stock': 25},
                {'name': 'Converse Chuck Taylor High', 'description': 'The classic high-top canvas sneaker, an eternal streetwear staple.', 'price': 2400000, 'discount_price': 2100000, 'stock': 30},
                {'name': 'Converse Weapon', 'description': 'A basketball-heritage sneaker reissued with modern comfort updates.', 'price': 3600000, 'discount_price': None, 'stock': 14},
                {'name': 'Converse Pro Leather', 'description': 'A leather basketball classic offering a clean, retro silhouette.', 'price': 3200000, 'discount_price': None, 'stock': 17},
                {'name': 'Converse Chuck 70 Hi', 'description': 'A high-top version of the Chuck 70 with premium canvas and vintage rubber detailing.', 'price': 2900000, 'discount_price': 2500000, 'stock': 21},
                {'name': 'Converse Star Player', 'description': 'A retro low-top featuring suede accents and a sporty, streamlined look.', 'price': 2500000, 'discount_price': None, 'stock': 23},
                {'name': 'Converse Chuck Taylor Platform', 'description': 'A raised-sole version of the classic Chuck for extra height and bold style.', 'price': 2700000, 'discount_price': None, 'stock': 19},
            ],
            'Vans': [
                {'name': 'Vans Old Skool', 'description': 'The iconic side-stripe skate shoe, durable and effortlessly stylish for any occasion.', 'price': 2500000, 'discount_price': None, 'stock': 30},
                {'name': 'Vans Sk8-Hi', 'description': 'A high-top skate classic offering extra ankle support without sacrificing timeless style.', 'price': 2900000, 'discount_price': 2500000, 'stock': 20},
                {'name': 'Vans Authentic', 'description': 'The original Vans silhouette — simple, durable canvas construction built for skating.', 'price': 2200000, 'discount_price': None, 'stock': 28},
                {'name': 'Vans Era', 'description': 'A padded-collar classic offering extra comfort while keeping the vintage Vans look.', 'price': 2300000, 'discount_price': None, 'stock': 26},
                {'name': 'Vans Slip-On', 'description': 'A checkerboard-pattern icon with an easy slip-on fit and laid-back California style.', 'price': 2400000, 'discount_price': 2100000, 'stock': 27},
                {'name': 'Vans Half Cab', 'description': 'A cropped high-top skate shoe designed for maximum board control and support.', 'price': 3000000, 'discount_price': None, 'stock': 16},
                {'name': 'Vans UltraRange', 'description': 'A cropped high-top skate shoe designed for maximum board control and support.', 'price': 3000000, 'discount_price': None, 'stock': 16},
                {'name': 'Vans UltraRange', 'description': 'A modern hybrid design combining skate DNA with plush comfort foam.', 'price': 3300000, 'discount_price': None, 'stock': 15},
                {'name': 'Vans Old Skool Platform', 'description': 'A raised-sole version of the Old Skool offering extra height and a bold stance.', 'price': 2800000, 'discount_price': 2400000, 'stock': 19},
                {'name': 'Vans Knu Skool', 'description': 'A chunky Y2K-inspired revival of the classic skate silhouette.', 'price': 3100000, 'discount_price': None, 'stock': 17},
                {'name': 'Vans Sk8-Hi Platform', 'description': 'A raised-sole take on the Sk8-Hi combining classic skate style with extra height.', 'price': 3200000, 'discount_price': None, 'stock': 16},
            ],
            'Jordan': [
                {'name': 'Air Jordan 1 High', 'description': 'The sneaker that started it all — bold colorways and premium leather in an unmistakable silhouette.', 'price': 6500000, 'discount_price': None, 'stock': 14},
                {'name': 'Air Jordan 4 Retro', 'description': 'A basketball legend featuring visible Air cushioning and iconic mesh side panels.', 'price': 7200000, 'discount_price': 6500000, 'stock': 10},
                {'name': 'Air Jordan 11', 'description': 'Patent leather shine meets carbon fiber support in one of the most beloved Jordans ever made.', 'price': 8500000, 'discount_price': None, 'stock': 8},
                {'name': 'Air Jordan 1 Low', 'description': 'A low-cut take on the original icon, offering the same style with everyday versatility.', 'price': 5200000, 'discount_price': 4600000, 'stock': 18},
                {'name': 'Air Jordan 3 Retro', 'description': 'Famous for its elephant print detailing and visible Air unit, a true basketball classic.', 'price': 7800000, 'discount_price': None, 'stock': 9},
                {'name': 'Air Jordan 6 Retro', 'description': 'Known for its performance heritage and iconic 1991 championship colorway.', 'price': 7500000, 'discount_price': 6800000, 'stock': 11},
                {'name': 'Air Jordan 5 Retro', 'description': 'Inspired by WWII fighter jets, featuring reflective tongue and translucent sole.', 'price': 7600000, 'discount_price': None, 'stock': 10},
                {'name': 'Air Jordan 12 Retro', 'description': 'A luxurious basketball silhouette featuring premium leather and a durable rubber sole.', 'price': 8200000, 'discount_price': None, 'stock': 7},
                {'name': 'Air Jordan 1 Mid', 'description': 'A mid-top balance between the High and Low, offering iconic style with everyday comfort.', 'price': 5800000, 'discount_price': 5200000, 'stock': 15},
                {'name': 'Air Jordan 13 Retro', 'description': 'Inspired by panther claws, featuring a holographic eyelet and plush cushioning.', 'price': 8000000, 'discount_price': None, 'stock': 8},
            ],
        }
        def create_products(products_list, category_name):
            category = categories[category_name]
            sizes_available = ['38', '39', '40', '41', '42', '43', '44']
            for i, prod_data in enumerate(products_list):
                slug = slugify(prod_data['name'])
                product, created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': category,
                        'name': prod_data['name'],
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'discount_price': prod_data['discount_price'],
                        'stock': prod_data['stock'],
                        'is_featured': i < 2,
                        'is_active': True,
                    }
                )
                if created:
                    for size in sizes_available:
                        ProductSize.objects.get_or_create(
                            product=product,
                            size=size,
                            defaults={'stock': prod_data['stock'] // len(sizes_available) + 2}
                        )
                    self.stdout.write(f"    [created] {prod_data['name']}")
                else:
                    self.stdout.write(f"    [exists] {prod_data['name']}")

        for brand_name, products_list in products_data.items():
            self.stdout.write(f"Adding {brand_name} products ({len(products_list)})...")
            create_products(products_list, brand_name)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Categories: {Category.objects.count()} | Products: {Product.objects.count()} | Sizes: {ProductSize.objects.count()}"
        ))
        self.stdout.write(self.style.WARNING("Note: Product images are empty. Add them from the Admin panel."))