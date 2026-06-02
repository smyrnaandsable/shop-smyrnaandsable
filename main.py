from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from tinydb import TinyDB, Query
import datetime

app = FastAPI()
db = TinyDB('db.json')

COLORS = {
    "bg": "#F5F0E8",
    "gold": "#C9A84C",
    "dark": "#2C2C2C",
    "text": "#4A4A4A",
    "light": "#FAF7F2"
}

PRODUCTS = [
    {
        "slug": "artichoke-tartlet",
        "name": "Artichoke & Andalouse Sauce Mousse Tartlet",
        "subtitle": "The Aegean Meets Belgium",
        "keynote": "Geographic Signified Urla Artichoke & Creamy Belgian Andalouse Mousse",
        "description": "A refined tartlet where the delicate, nutty flavour of Urla's geographically protected artichoke meets the bold creaminess of Belgian Andalouse mousse. Each bite is a bridge between the Aegean coastline and the bold flavors of Belgium."
    },
    {
        "slug": "golden-connection",
        "name": "Golden Connection: Ödemiş Potato & Herve Cheese Gratin",
        "subtitle": "A True Golden Connection",
        "keynote": "Mandolin-sliced Ödemiş Potatoes & Heritage Belgian Herve Cheese",
        "description": "Layers of mandolin-sliced Ödemiş potatoes, celebrated across Turkey's countryside, meet the pungent depth of Heritage Belgian Herve Cheese. Served in a stone-baked tradition."
    },
    {
        "slug": "lemon-sable",
        "name": "Aegean Sunshine: Lemon & White Chocolate Sablé",
        "subtitle": "The Harmony of Sun and Cream",
        "keynote": "Fresh Lemon Zest & Premium Belgian White Chocolate",
        "description": "Sun-kissed lemon zest from the Aegean coast meets premium Belgian white chocolate ganache, creating a perfect balance of zesty freshness and velvet sweetness. A true tribute to the sunny coasts of İzmir and the master chocolatiers of Belgium."
    },
    {
        "slug": "boyoz-chocolate",
        "name": "Belgian Chocolate Boyoz",
        "subtitle": "The Meeting of Classics",
        "keynote": "Traditional İzmir Boyoz & Premium Belgian Chocolate",
        "description": "The iconic flaky pastry of İzmir, reimagined with a molten core of premium Belgian chocolate. Perfectly paired with a foamy Turkish coffee, it offers a moment of pure nostalgia and refined taste."
    },
    {
        "slug": "kumru-croissant",
        "name": "Kumru-Vasan: The Aegean Croissant",
        "subtitle": "East Meets West at Breakfast",
        "keynote": "Flaky Belgian Croissant & Traditional İzmir Tulum Cheese",
        "description": "The beloved Kumru sandwich of İzmir, reimagined in the form of a flaky Belgian croissant filled with traditional Tulum cheese, fresh tomato, and the option of artisanal Jambon d'Ardenne — celebrating the diversity of choice in a spirit of mutual respect and openness."
    },
    {
        "slug": "speculoos-boyoz",
        "name": "Speculoos & Cinnamon Boyoz",
        "subtitle": "Spice Routes Reconnected",
        "keynote": "Flaky Traditional Boyoz & Molten Belgian Speculoos Cream",
        "description": "Traditional İzmir boyoz pastry reimagined with a warm, molten filling of Belgian Speculoos cream and cinnamon. A sensory journey along ancient spice routes, now reunited in every flaky, golden bite."
    }
]

BASE_STYLES = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    background-color: #F5F0E8; 
    font-family: 'Georgia', serif; 
    color: #4A4A4A;
    min-height: 100vh;
}
.header {
    background-color: #FAF7F2;
    border-bottom: 1px solid #C9A84C;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.logo {
    font-size: 18px;
    font-weight: bold;
    color: #2C2C2C;
    letter-spacing: 2px;
    text-decoration: none;
}
.logo span { color: #C9A84C; }
.concept-badge {
    font-size: 10px;
    color: #C9A84C;
    border: 1px solid #C9A84C;
    padding: 3px 8px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.consent-banner {
    background-color: #2C2C2C;
    color: #FAF7F2;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    gap: 12px;
    flex-wrap: wrap;
}
.consent-banner p { flex: 1; line-height: 1.5; }
.consent-btn {
    background-color: #C9A84C;
    color: #2C2C2C;
    border: none;
    padding: 8px 18px;
    font-size: 12px;
    cursor: pointer;
    letter-spacing: 1px;
    font-family: 'Georgia', serif;
    white-space: nowrap;
}
.container { max-width: 960px; margin: 0 auto; padding: 40px 24px; }
.disclaimer {
    background-color: #FAF7F2;
    border-left: 3px solid #C9A84C;
    padding: 12px 18px;
    font-size: 12px;
    color: #4A4A4A;
    margin-bottom: 40px;
    line-height: 1.6;
}
.page-title {
    font-size: 28px;
    color: #2C2C2C;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.page-subtitle {
    color: #C9A84C;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 40px;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}
.card {
    background-color: #FAF7F2;
    border: 1px solid #E8E0D0;
    padding: 28px 24px;
    text-decoration: none;
    display: block;
    transition: border-color 0.2s;
}
.card:hover { border-color: #C9A84C; }
.card-number {
    font-size: 11px;
    color: #C9A84C;
    letter-spacing: 2px;
    margin-bottom: 12px;
}
.card-title {
    font-size: 16px;
    color: #2C2C2C;
    margin-bottom: 8px;
    line-height: 1.4;
}
.card-subtitle {
    font-size: 12px;
    color: #C9A84C;
    letter-spacing: 1px;
    margin-bottom: 14px;
    font-style: italic;
}
.card-keynote {
    font-size: 11px;
    color: #4A4A4A;
    line-height: 1.5;
    border-top: 1px solid #E8E0D0;
    padding-top: 14px;
}
.card-keynote strong { color: #C9A84C; }
.inquire-btn {
    display: inline-block;
    margin-top: 18px;
    padding: 10px 20px;
    border: 1px solid #C9A84C;
    color: #2C2C2C;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-decoration: none;
    font-family: 'Georgia', serif;
}
.footer {
    text-align: center;
    padding: 32px 24px;
    font-size: 11px;
    color: #9A9A9A;
    border-top: 1px solid #E8E0D0;
    letter-spacing: 1px;
}
.back-link {
    display: inline-block;
    margin-bottom: 28px;
    font-size: 12px;
    color: #C9A84C;
    text-decoration: none;
    letter-spacing: 1px;
}
.product-title {
    font-size: 26px;
    color: #2C2C2C;
    margin-bottom: 8px;
    line-height: 1.3;
}
.product-subtitle {
    color: #C9A84C;
    font-size: 14px;
    letter-spacing: 2px;
    font-style: italic;
    margin-bottom: 28px;
}
.product-desc {
    font-size: 15px;
    line-height: 1.8;
    color: #4A4A4A;
    margin-bottom: 28px;
}
.keynote-box {
    background-color: #FAF7F2;
    border-left: 3px solid #C9A84C;
    padding: 16px 20px;
    font-size: 13px;
    color: #2C2C2C;
    margin-bottom: 32px;
    line-height: 1.6;
}
.keynote-box strong { color: #C9A84C; }
.contact-box {
    background-color: #2C2C2C;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 32px;
}
.contact-box p {
    color: #FAF7F2;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 16px;
}
.contact-box a {
    display: inline-block;
    background-color: #C9A84C;
    color: #2C2C2C;
    padding: 12px 28px;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-decoration: none;
    font-family: 'Georgia', serif;
}
"""

CONSENT_SCRIPT = """
<script>
function acceptConsent() {
    document.cookie = "consent_status=granted; path=/; max-age=31536000";
    document.getElementById('consent-banner').style.display = 'none';
}
function declineConsent() {
    document.cookie = "consent_status=denied; path=/; max-age=31536000";
    document.getElementById('consent-banner').style.display = 'none';
}
window.onload = function() {
    var cookies = document.cookie;
    if (cookies.indexOf('consent_status=granted') !== -1 || cookies.indexOf('consent_status=denied') !== -1) {
        var b = document.getElementById('consent-banner');
        if (b) b.style.display = 'none';
    }
}
</script>
"""

def consent_banner_html():
    return """
    <div class="consent-banner" id="consent-banner">
        <p>We use cookies to ensure GDPR compliance and improve your experience. 
        You have the right to accept or decline non-essential cookies.</p>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button class="consent-btn" onclick="acceptConsent()">Accept</button>
            <button class="consent-btn" style="background-color:transparent; color:#FAF7F2; border:1px solid #FAF7F2;" onclick="declineConsent()">Decline</button>
        </div>
    </div>
    """

def header_html(show_back=False):
    back = '<a href="/" class="back-link">← Back to Collection</a>' if show_back else ""
    return f"""
    <header class="header">
        <a href="/" class="logo">SMYRNA <span>&</span> SABLE</a>
        <span class="concept-badge">Concept Collection</span>
    </header>
    {consent_banner_html()}
    """

def disclaimer_html():
    return """
    <div class="disclaimer">
        <strong>Transparency Note:</strong> Smyrna & Sable is a brand concept developed to 
        demonstrate full-cycle marketing integration and international market entry strategies. 
        These products are conceptual and not available for commercial purchase.
    </div>
    """

def footer_html():
    return """
    <footer class="footer">
        <p>© 2026 Smyrna & Sable · Designed with Passion in İzmir · Protected by Sovereign Core</p>
    </footer>
    """

@app.middleware("http")
async def sovereign_protection(request: Request, call_next):
    user_agent = request.headers.get("user-agent", "").lower()
    if "bot" in user_agent or "python-requests" in user_agent:
        db.insert({
            "type": "bot_blocked",
            "path": str(request.url.path),
            "timestamp": datetime.datetime.now().isoformat()
        })
        return Response(content="Access Denied", status_code=403)
    consent_status = request.cookies.get("consent_status", "denied")
    db.insert({
        "type": "visit",
        "path": str(request.url.path),
        "consent": consent_status,
        "timestamp": datetime.datetime.now().isoformat()
    })
    response = await call_next(request)
    response.headers["X-Consent-Status"] = consent_status
    response.headers["X-Protected-By"] = "Sovereign Core"
    return response

@app.get("/")
async def root():
    cards_html = ""
    for i, p in enumerate(PRODUCTS):
        cards_html += f"""
        <a href="/product/{p['slug']}" class="card">
            <div class="card-number">0{i+1}</div>
            <div class="card-title">{p['name']}</div>
            <div class="card-subtitle">{p['subtitle']}</div>
            <div class="card-keynote"><strong>Key Note:</strong> {p['keynote']}</div>
            <span class="inquire-btn">Inquire Now</span>
        </a>
        """
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smyrna & Sable — Concept Collection</title>
            <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-TX9JGWML');</script>
    <!-- End Google Tag Manager -->
        <style>{BASE_STYLES}</style>
        {CONSENT_SCRIPT}
    </head>
    <body>
                <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TX9JGWML"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
        {header_html()}
        <div class="container">
            {disclaimer_html()}
            <h1 class="page-title">The Collection</h1>
            <p class="page-subtitle">İzmir & Belgium — A Fusion of Two Worlds</p>
            <div class="grid">{cards_html}</div>
        </div>
        {footer_html()}
    </body>
    </html>
    """)

@app.get("/product/{slug}")
async def product_page(slug: str):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        return HTMLResponse(content="<h1>Product not found</h1>", status_code=404)
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{product['name']} — Smyrna & Sable</title>
            <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-TX9JGWML');</script>
    <!-- End Google Tag Manager -->
        <style>{BASE_STYLES}</style>
        {CONSENT_SCRIPT}
    </head>
    <body>
                <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TX9JGWML"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
        {header_html(show_back=True)}
        <div class="container">
            <a href="/" class="back-link">← Back to Collection</a>
            {disclaimer_html()}
            <h1 class="product-title">{product['name']}</h1>
            <p class="product-subtitle">{product['subtitle']}</p>
            <p class="product-desc">{product['description']}</p>
            <div class="keynote-box">
                <strong>Key Note:</strong> {product['keynote']}
            </div>
            <div class="contact-box">
                <p>Interested in this concept or our MarTech capabilities?<br>
                We'd love to hear from you.</p>
                <a href="mailto:contact@smyrnaandsable.com">Get in Touch</a>
            </div>
        </div>
        {footer_html()}
    </body>
    </html>
    """)

@app.get("/health")
async def health():
    visits = db.all()
    total = len(visits)
    blocked = len([v for v in visits if v.get("type") == "bot_blocked"])
    return {
        "status": "Sovereign Core Active",
        "total_traffic": total,
        "bots_blocked": blocked,
        "timestamp": datetime.datetime.now().isoformat()
    }