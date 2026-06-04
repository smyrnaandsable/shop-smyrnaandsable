from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from tinydb import TinyDB, Query
import datetime

app = FastAPI()
db = TinyDB('db.json')

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
    flex-wrap: wrap;
    gap: 10px;
}
.logo {
    font-size: 18px;
    font-weight: bold;
    color: #2C2C2C;
    letter-spacing: 2px;
    text-decoration: none;
}
.logo span { color: #C9A84C; }
.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.lang-switcher {
    display: flex;
    gap: 8px;
}
.lang-btn {
    font-size: 11px;
    color: #9A9A9A;
    text-decoration: none;
    letter-spacing: 1px;
    padding: 3px 6px;
    border: 1px solid transparent;
}
.lang-btn.active {
    color: #C9A84C;
    border-color: #C9A84C;
}
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
.consent-btns { display: flex; gap: 10px; flex-wrap: wrap; }
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
.consent-btn.decline {
    background-color: transparent;
    color: #FAF7F2;
    border: 1px solid #FAF7F2;
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
.card-number { font-size: 11px; color: #C9A84C; letter-spacing: 2px; margin-bottom: 12px; }
.card-title { font-size: 16px; color: #2C2C2C; margin-bottom: 8px; line-height: 1.4; }
.card-subtitle { font-size: 12px; color: #C9A84C; letter-spacing: 1px; margin-bottom: 14px; font-style: italic; }
.card-keynote { font-size: 11px; color: #4A4A4A; line-height: 1.5; border-top: 1px solid #E8E0D0; padding-top: 14px; }
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
.back-link { display: inline-block; margin-bottom: 28px; font-size: 12px; color: #C9A84C; text-decoration: none; letter-spacing: 1px; }
.product-title { font-size: 26px; color: #2C2C2C; margin-bottom: 8px; line-height: 1.3; }
.product-subtitle { color: #C9A84C; font-size: 14px; letter-spacing: 2px; font-style: italic; margin-bottom: 8px; }
.product-tagline { font-size: 13px; color: #2C2C2C; letter-spacing: 1px; margin-bottom: 28px; font-style: italic; }
.product-desc { font-size: 15px; line-height: 1.8; color: #4A4A4A; margin-bottom: 28px; }
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
.contact-box p { color: #FAF7F2; font-size: 13px; line-height: 1.7; margin-bottom: 16px; }
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

GTM_HEAD = """    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-TX9JGWML');</script>
    <!-- End Google Tag Manager -->"""

GTM_BODY = """        <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TX9JGWML"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->"""

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

CONSENT_TEXT = {
    "en": "We use cookies to ensure GDPR compliance and improve your experience. You have the right to accept or decline non-essential cookies.",
    "fr": "Nous utilisons des cookies pour assurer la conformité au RGPD et améliorer votre expérience. Vous avez le droit d'accepter ou de refuser les cookies non essentiels.",
    "nl": "Wij gebruiken cookies om GDPR-naleving te garanderen en uw ervaring te verbeteren. U heeft het recht om niet-essentiële cookies te accepteren of te weigeren."
}

ACCEPT_TEXT = {"en": "Accept", "fr": "Accepter", "nl": "Accepteren"}
DECLINE_TEXT = {"en": "Decline", "fr": "Refuser", "nl": "Weigeren"}
BACK_TEXT = {"en": "← Back to Collection", "fr": "← Retour à la Collection", "nl": "← Terug naar Collectie"}
INQUIRE_TEXT = {"en": "Inquire Now", "fr": "Renseignez-vous", "nl": "Informeer Nu"}
CONTACT_TEXT = {
    "en": ("Interested in this concept or our MarTech capabilities?<br>We'd love to hear from you.", "Get in Touch"),
    "fr": ("Intéressé par ce concept ou nos capacités MarTech?<br>Nous serions ravis de vous entendre.", "Contactez-nous"),
    "nl": ("Geïnteresseerd in dit concept of onze MarTech-mogelijkheden?<br>We horen graag van u.", "Neem Contact Op")
}
DISCLAIMER_TEXT = {
    "en": "<strong>Transparency Note:</strong> Smyrna & Sable is a brand concept developed to demonstrate full-cycle marketing integration and international market entry strategies. These products are conceptual and not available for commercial purchase.",
    "fr": "<strong>Note de Transparence :</strong> Smyrna & Sable est un concept de marque développé pour démontrer une intégration marketing complète et des stratégies d'entrée sur le marché international. Ces produits sont conceptuels et ne sont pas disponibles à l'achat commercial.",
    "nl": "<strong>Transparantienota:</strong> Smyrna & Sable is een merkconcept ontwikkeld om volledige marketingintegratie en internationale marktintredestrategieën te demonstreren. Deze producten zijn conceptueel en niet beschikbaar voor commerciële aankoop."
}
COLLECTION_TITLE = {"en": "The Collection", "fr": "La Collection", "nl": "De Collectie"}
COLLECTION_SUBTITLE = {"en": "İzmir & Belgium — A Fusion of Two Worlds", "fr": "İzmir & Belgique — Une Fusion de Deux Mondes", "nl": "İzmir & België — Een Fusie van Twee Werelden"}

PRODUCTS = {
    "kumru-croissant": {
        "en": {
            "name": "Kumru-Vasan: The Aegean Croissant",
            "subtitle": "Where the Simplicity of İzmir Kumru Meets the Elegance of Belgian Croissant",
            "tagline": "A Fusion of Authenticity and Craftsmanship",
            "description": "More than a sandwich, Kumru-vasan is a heartfelt dialogue between two vibrant cultures. We start with the flaky, buttery layers of a premier Belgian croissant, baked to a golden crisp. Its heart, however, belongs to İzmir: the legendary authentic tulum cheese, fresh tomato slices, and a whole green pepper. This unique creation honors tradition while embracing modern tastes. In line with our inclusive vision, we invite you to personalize your journey by opting for a delicate layer of artisanal Jambon d'Ardenne, celebrating the diversity of choice in a spirit of mutual respect and openness.",
            "keynote": "Flaky Belgian Croissant & Traditional İzmir Tulum Cheese. Optional: Artisanal Jambon d'Ardenne."
        },
        "fr": {
            "name": "Kumru-Vasan: The Aegean Croissant",
            "subtitle": "Où la Simplicité du Kumru d'İzmir rencontre l'Élégance du Croissant Belge",
            "tagline": "Une Fusion d'Authenticité et d'Artisanat",
            "description": "Plus qu'un sandwich, le Kumru-vasan est un dialogue sincère entre deux cultures vibrantes. Nous commençons par les couches feuilletées et beurrées d'un croissant belge de premier choix, cuit jusqu'à obtenir un croustillant doré. Son cœur, cependant, appartient à Izmir : le légendaire fromage tulum authentique, des tranches de tomates fraîches et un piment vert entier. Cette création unique honore la tradition tout en embrassant les goûts modernes. Fidèles à notre vision inclusive, nous vous invitons à personnaliser votre voyage en optant pour une délicate couche de Jambon d'Ardenne artisanal, célébrant la diversité des choix dans un esprit de respect mutuel et d'ouverture.",
            "keynote": "Croissant Belge Feuilleté & Fromage Tulum Traditionnel d'İzmir. En option : Jambon d'Ardenne artisanal."
        },
        "nl": {
            "name": "Kumru-Vasan: The Aegean Croissant",
            "subtitle": "Waar de Eenvoud van İzmir Kumru de Elegantie van Belgische Croissant ontmoet",
            "tagline": "Een Fusie van Authenticiteit en Vakmanschap",
            "description": "Meer dan een sandwich, is de Kumru-vasan een oprechte dialoog tussen twee levendige culturen. We beginnen met de knapperige, boterachtige laagjes van een premium Belgische croissant, gebakken tot een gouden perfectie. Het hart behoort echter toe aan İzmir: de legendarische authentieke tulum kaas, verse tomatenschijfjes en een hele groene peper. Deze unieke creatie eert traditie terwijl ze moderne smaken omarmt. In lijn met onze inclusieve visie, nodigen we u uit om uw reis te personaliseren door te kiezen voor een delicaate laag ambachtelijke Jambon d'Ardenne, waarbij we de diversiteit van keuze vieren in een geest van wederzijds respect en openheid.",
            "keynote": "Knapperige Belgische Croissant & Traditionele İzmir Tulum Kaas. Optioneel: Ambachtelijke Jambon d'Ardenne."
        }
    },
    "speculoos-boyoz": {
        "en": {
            "name": "Speculoos & Cinnamon Boyoz",
            "subtitle": "Souvenirs d'Enfance",
            "tagline": "A Nostalgic Embrace",
            "description": "More than a pastry, 'Souvenirs d'Enfance' is a nostalgic embrace. We begin with the authentic, incredibly flaky layers of a traditional İzmir Boyoz, a puff pastry baked to golden perfection. Its heart, however, beats with the beloved flavor of Belgium: a rich, melt-in-the-mouth center of molten Speculoos cream, subtly caramelized and kissed with warm cinnamon. This unique synthesis evokes the cherished warmth of a mother's kitchen, inviting even the most discerning palate to rediscover the pure joy of childhood memories.",
            "keynote": "Flaky traditional Boyoz & Molten Belgian Speculoos cream."
        },
        "fr": {
            "name": "Speculoos & Cinnamon Boyoz",
            "subtitle": "Un Voyage Doux au Cœur de l'Enfance",
            "tagline": "Une Étreinte Nostalgique",
            "description": "Plus qu'une pâtisserie, 'Souvenirs d'Enfance' est une étreinte nostalgique. Nous commençons par les couches authentiques et incroyablement croustillantes d'un Boyoz traditionnel d'Izmir, une pâte feuilletée cuite à la perfection dorée. Son cœur, cependant, bat au rythme de la saveur chérie de la Belgique : un centre riche et fondant de crème de Speculoos fondue, subtilement caramélisée et effleurée de cannelle chaude. Cette synthèse unique évoque la chaleur précieuse de la cuisine d'une mère, invitant même les palais les plus exigeants à redécouvrir la pure joie des souvenirs d'enfance.",
            "keynote": "Boyoz traditionnel croustillant & Crème de Speculoos belge fondue."
        },
        "nl": {
            "name": "Speculoos & Cinnamon Boyoz",
            "subtitle": "Een Nostalgische Reis naar de Geborgenheid van Thuis",
            "tagline": "Een Nostalgische Omhelzing",
            "description": "Meer dan een gebakje, is 'Souvenirs d'Enfance' een nostalgische omhelzing. We beginnen met de authentieke, ongelooflijk knapperige laagjes van een traditionele İzmir Boyoz, een bladerdeeg gebakken tot gouden perfectie. Het hart klopt echter met de geliefde smaak van België: een rijke, smelt-in-de-mond kern van vloeibare Speculoos crème, subtiel gekarameliseerd en gekust met warme kaneel. Deze unieke synthese roept de gekoesterde warmte op van een moeders keuken, en nodigt zelfs de meest veeleisende fijnproever uit om de pure vreugde van jeugdherinneringen te herontdekken.",
            "keynote": "Knapperige traditionele Boyoz & Vloeibare Belgische Speculoos crème."
        }
    },
    "lemon-sable": {
        "en": {
            "name": "Aegean Sunshine: Lemon & White Chocolate Sablé",
            "subtitle": "The Harmony of Sun and Cream",
            "tagline": "East Meets West in Every Bite",
            "description": "Experience the ultimate fusion of East and West. Our signature buttery Sable biscuit is infused with fresh Aegean lemon zest, offering a crisp, citrusy awakening. At its heart lies a silky layer of premium Belgian white chocolate ganache, creating a perfect balance of zesty freshness and velvet sweetness. A true tribute to the sunny coasts of İzmir and the master chocolatiers of Belgium.",
            "keynote": "Fresh lemon zest & Premium Belgian white chocolate."
        },
        "fr": {
            "name": "Aegean Sunshine: Lemon & White Chocolate Sablé",
            "subtitle": "L'Éclat du Soleil Égéen",
            "tagline": "L'Orient rencontre l'Occident à chaque bouchée",
            "description": "Découvrez une fusion exquise entre l'Orient et l'Occident. Notre sablé pur beurre est infusé de zestes de citron frais de l'Égée, offrant un éveil croustillant et citronné. En son cœur se cache une couche soyeuse de ganache au chocolat blanc belge de qualité supérieure, créant un équilibre parfait entre fraîcheur acidulée et douceur veloutée. Un véritable hommage aux côtes ensoleillées d'Izmir et aux maîtres chocolatiers belges.",
            "keynote": "Zestes de citron frais et chocolat blanc belge premium."
        },
        "nl": {
            "name": "Aegean Sunshine: Lemon & White Chocolate Sablé",
            "subtitle": "De Gloed van de Egeïsche Zon",
            "tagline": "Oost ontmoet West in elke hap",
            "description": "Ervaar de ultieme fusie tussen Oost en West. Ons karakteristieke roomboter-sablé koekje is doordrenkt met verse Egeïsche citroenrasp voor een frisse, knapperige beleving. De kern bestaat uit een zijdezachte laag premium Belgische witte chocoladeganache, wat zorgt voor de perfecte balans tussen citrusfrisheid en fluweelzachte zoetheid. Een eerbetoon aan de zonnige kusten van İzmir en het vakmanschap van de Belgische chocolatiers.",
            "keynote": "Verse citroenrasp & Premium Belgische witte chocolade."
        }
    },
    "boyoz-chocolate": {
        "en": {
            "name": "Belgian Chocolate Boyoz",
            "subtitle": "The Meeting of Classics",
            "tagline": "Where Two Worlds Become One",
            "description": "A legendary encounter between two worlds. The authentic, golden layers of traditional İzmir Boyoz meet the rich, velvety soul of premium Belgian chocolate. This is where the crispy heritage of the Aegean meets the world-renowned mastery of Belgian chocolatiers. Perfectly paired with a foamy Turkish coffee, it offers a moment of pure nostalgia and refined taste.",
            "keynote": "Traditional İzmir Boyoz & Premium Belgian Chocolate."
        },
        "fr": {
            "name": "Belgian Chocolate Boyoz",
            "subtitle": "La Rencontre des Classiques",
            "tagline": "Quand Deux Mondes n'en Font qu'Un",
            "description": "Une rencontre légendaire entre deux mondes. Les couches dorées et authentiques du Boyoz traditionnel d'Izmir rencontrent l'âme riche et veloutée du chocolat belge de qualité supérieure. C'est ici que l'héritage croustillant de l'Égée rencontre la maîtrise mondiale des chocolatiers belges. Accompagné parfaitement d'un café turc mousseux, il offre un moment de pure nostalgie et de goût raffiné.",
            "keynote": "Boyoz traditionnel d'Izmir et chocolat belge premium."
        },
        "nl": {
            "name": "Belgian Chocolate Boyoz",
            "subtitle": "De Ontmoeting van Klassiekers",
            "tagline": "Waar Twee Werelden Één Worden",
            "description": "Een legendarische ontmoeting tussen twee werelden. De authentieke, gouden laagjes van de traditionele İzmir Boyoz ontmoeten de rijke, fluweelzachte ziel van premium Belgische chocolade. Hier ontmoet het knapperige erfgoed van de Egeïsche kust het wereldberoemde vakmanschap van de Belgische chocolatiers. Perfect in combinatie met een schuimige Turkse koffie, biedt het een moment van pure nostalgie en verfijnde smaak.",
            "keynote": "Traditionele İzmir Boyoz & Premium Belgische chocolade."
        }
    },
    "artichoke-tartlet": {
        "en": {
            "name": "Artichoke & Andalouse Sauce Mousse Tartlet",
            "subtitle": "Where Urla's Heritage Meets Belgian Character",
            "tagline": "The Peak of Mediterranean Sophistication",
            "description": "A true masterpiece of culinary fusion. We take the world-renowned, protected 'Sakız' artichokes from Urla's fertile lands and transform them into a silky, pastel-green mousse. This delicate heart is nestled within a crisp, golden tartlet shell and crowned with a sophisticated touch of Belgian Andalouse sauce. Finished with a drop of premium Aegean olive oil and a sprig of fresh thyme, it offers a refined journey between the sun-drenched coasts of Izmir and the bold flavors of Belgium.",
            "keynote": "Geographic Signified Urla Artichoke & Creamy Belgian Andalouse Mousse."
        },
        "fr": {
            "name": "Artichoke & Andalouse Sauce Mousse Tartlet",
            "subtitle": "Où le Patrimoine d'Urla rencontre le Caractère Belge",
            "tagline": "Le Sommet de la Sophistication Méditerranéenne",
            "description": "Un véritable chef-d'œuvre de fusion culinaire. Nous prenons les célèbres artichauts 'Sakız' d'Urla, protégés et issus de terres fertiles, pour les transformer en une mousse soyeuse d'un vert pastel. Ce cœur délicat est niché dans une coque de tartelette dorée et croustillante, couronnée d'une touche sophistiquée de sauce Andalouse belge. Agrémentée d'une goutte d'huile d'olive de qualité supérieure de l'Égée et d'un brin de thym frais, elle offre un voyage raffiné entre les côtes ensoleillées d'Izmir et les saveurs audacieuses de la Belgique.",
            "keynote": "Artichaut d'Urla (IGP) et Mousse Crémeuse à l'Andalouse Belge."
        },
        "nl": {
            "name": "Artichoke & Andalouse Sauce Mousse Tartlet",
            "subtitle": "Waar het Erfgoed van Urla het Belgische Karakter ontmoet",
            "tagline": "Het Hoogtepunt van Mediterrane Verfijning",
            "description": "Een waar meesterwerk van culinaire fusie. We nemen de wereldberoemde, beschermde 'Sakız' artisjokken van de vruchtbare gronden van Urla en transformeren ze in een zijdezachte, pastelgroene mousse. Dit delicate hart rust in een brosse, gouden taartbodem en wordt bekroond met een verfijnd vleugje Belgische Andalousesaus. Afgewerkt met een druppel premium Egeïsche olijfolie en een takje verse tijm, biedt het een verfijnde reis tussen de zonovergoten kusten van Izmir en de gedurfde smaken van België.",
            "keynote": "Geografisch Gekentekende Urla Artisjok & Romige Belgische Andalouse Mousse."
        }
    },
    "golden-connection": {
        "en": {
            "name": "Golden Connection: Ödemiş Potato & Herve Cheese Gratin",
            "subtitle": "A Golden Bond Between Two Rich Soils",
            "tagline": "The Ultimate Comfort of Two Traditions",
            "description": "A rustic masterpiece that celebrates the golden treasures of two lands. We start with the world-famous, sun-colored potatoes from the fertile soils of Ödemiş, sliced to mandolin perfection. These layers are slow-baked in a rich cream infused with the bold, UNESCO-protected Herve Cheese from Belgium. The result is a melting, golden-crusted gratin that bridges the warmth of an Aegean farm with the artisanal dairy heritage of the Belgian countryside. A true 'Golden Connection' served in a stone-baked tradition.",
            "keynote": "Mandolin-sliced Ödemiş Potatoes & Heritage Belgian Herve Cheese."
        },
        "fr": {
            "name": "Golden Connection: Ödemiş Potato & Herve Cheese Gratin",
            "subtitle": "Un Lien Doré Entre Deux Terres Riches",
            "tagline": "Le Confort Ultime de Deux Traditions",
            "description": "Un chef-d'œuvre rustique qui célèbre les trésors dorés de deux terroirs. Nous commençons par les célèbres pommes de terre couleur soleil des terres fertiles d'Ödemiş, tranchées avec une précision mandoline. Ces couches sont cuites lentement dans une crème onctueuse infusée au caractère affirmé du Fromage de Herve belge, protégé par l'UNESCO. Le résultat est un gratin fondant à la croûte dorée, créant un pont entre la chaleur d'une ferme égéenne et l'héritage laitier artisanal de la campagne belge. Une véritable 'Connexion Dorée' servie dans la tradition de la pierre.",
            "keynote": "Pommes de terre d'Ödemiş tranchées à la mandoline et fromage de Herve belge traditionnel."
        },
        "nl": {
            "name": "Golden Connection: Ödemiş Potato & Herve Cheese Gratin",
            "subtitle": "Een Gouden Band Tussen Twee Rijke Gronden",
            "tagline": "Het Ultieme Comfort van Twee Tradities",
            "description": "Een rustiek meesterwerk dat de gouden schatten van twee landen viert. We beginnen met de wereldberoemde, zonkleurige aardappelen van de vruchtbare gronden van Ödemiş, in flinterdunne mandoline-schijfjes gesneden. Deze laagjes worden langzaam gebakken in een rijke room, doordrenkt met de karaktervolle, door UNESCO beschermde Herve Kaas uit België. Het resultaat is een smeltende gratin met een goudbruine korst die de warmte van een Egeïsche boerderij verbindt met het ambachtelijke zuivelverleden van het Belgische platteland. Een echte 'Gouden Verbinding', geserveerd volgens de traditie van het steenbakken.",
            "keynote": "Mandoline-gesneden Ödemiş Aardappelen & Ambachtelijke Belgische Herve Kaas."
        }
    }
}

PRODUCT_ORDER = ["artichoke-tartlet", "golden-connection", "lemon-sable", "boyoz-chocolate", "kumru-croissant", "speculoos-boyoz"]

def get_lang(lang):
    if lang not in ["en", "fr", "nl"]:
        return "en"
    return lang

def lang_url(slug, lang, current_lang):
    active = "active" if lang == current_lang else ""
    return f'<a href="/product/{slug}/{lang}" class="lang-btn {active}">{lang.upper()}</a>'

def home_lang_url(lang, current_lang):
    active = "active" if lang == current_lang else ""
    return f'<a href="/{lang}" class="lang-btn {active}">{lang.upper()}</a>'

def render_page(title, body, lang="en", slug=None):
    if slug:
        lang_switch = lang_url(slug, "en", lang) + lang_url(slug, "fr", lang) + lang_url(slug, "nl", lang)
    else:
        lang_switch = home_lang_url("en", lang) + home_lang_url("fr", lang) + home_lang_url("nl", lang)

    consent_p = CONSENT_TEXT[lang]
    accept = ACCEPT_TEXT[lang]
    decline = DECLINE_TEXT[lang]

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Smyrna & Sable</title>
    {GTM_HEAD}
    <style>{BASE_STYLES}</style>
    {CONSENT_SCRIPT}
</head>
<body>
    {GTM_BODY}
    <div class="consent-banner" id="consent-banner">
        <p>{consent_p}</p>
        <div class="consent-btns">
            <button class="consent-btn" onclick="acceptConsent()">{accept}</button>
            <button class="consent-btn decline" onclick="declineConsent()">{decline}</button>
        </div>
    </div>
    <header class="header">
        <a href="/{lang}" class="logo">SMYRNA <span>&</span> SABLE</a>
        <div class="header-right">
            <div class="lang-switcher">{lang_switch}</div>
            <span class="concept-badge">Concept</span>
        </div>
    </header>
    {body}
    <footer class="footer">
        <p>© 2026 Smyrna & Sable · İzmir & Belgium · Protected by Sovereign Core</p>
    </footer>
</body>
</html>"""


@app.get("/robots.txt")
async def robots():
    return Response(content="""User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: https://shop.smyrnaandsable.com/sitemap.xml
""", media_type="text/plain")

@app.get("/sitemap.xml")
async def sitemap():
    urls = []
    for slug in PRODUCT_ORDER:
        for lang in ["en", "fr", "nl"]:
            urls.append(f"https://shop.smyrnaandsable.com/product/{slug}/{lang}")
    for lang in ["en", "fr", "nl"]:
        urls.append(f"https://shop.smyrnaandsable.com/{lang}")
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>{url}</loc></url>\n'
    xml += '</urlset>'
    return Response(content=xml, media_type="application/xml")

@app.middleware("http")
async def sovereign_protection(request: Request, call_next):
    user_agent = request.headers.get("user-agent", "").lower()
    if "python-requests" in user_agent or "scrapy" in user_agent:
        db.insert({"type": "bot_blocked", "path": str(request.url.path), "timestamp": datetime.datetime.now().isoformat()})
        return Response(content="Access Denied", status_code=403)
    consent_status = request.cookies.get("consent_status", "denied")
    db.insert({"type": "visit", "path": str(request.url.path), "consent": consent_status, "timestamp": datetime.datetime.now().isoformat()})
    response = await call_next(request)
    response.headers["X-Consent-Status"] = consent_status
    response.headers["X-Protected-By"] = "Sovereign Core"
    return response

@app.get("/")
async def root():
    return await home("en")

@app.get("/{lang}")
async def home(lang: str):
    if lang not in ["en", "fr", "nl"]:
        return HTMLResponse(content="Not found", status_code=404)
    
    cards = ""
    for i, slug in enumerate(PRODUCT_ORDER):
        p = PRODUCTS[slug][lang]
        cards += f"""
        <a href="/product/{slug}/{lang}" class="card">
            <div class="card-number">0{i+1}</div>
            <div class="card-title">{p['name']}</div>
            <div class="card-subtitle">{p['subtitle']}</div>
            <div class="card-keynote"><strong>Key Note:</strong> {p['keynote']}</div>
            <span class="inquire-btn">{INQUIRE_TEXT[lang]}</span>
        </a>"""

    body = f"""
    <div class="container">
        <div class="disclaimer">{DISCLAIMER_TEXT[lang]}</div>
        <h1 class="page-title">{COLLECTION_TITLE[lang]}</h1>
        <p class="page-subtitle">{COLLECTION_SUBTITLE[lang]}</p>
        <div class="grid">{cards}</div>
    </div>"""

    return HTMLResponse(content=render_page(COLLECTION_TITLE[lang], body, lang))

@app.get("/product/{slug}/{lang}")
async def product_page(slug: str, lang: str):
    lang = get_lang(lang)
    if slug not in PRODUCTS:
        return HTMLResponse(content="Not found", status_code=404)
    
    p = PRODUCTS[slug][lang]
    contact_p, contact_btn = CONTACT_TEXT[lang]

    body = f"""
    <div class="container">
        <a href="/{lang}" class="back-link">{BACK_TEXT[lang]}</a>
        <div class="disclaimer">{DISCLAIMER_TEXT[lang]}</div>
        <h1 class="product-title">{p['name']}</h1>
        <p class="product-subtitle">{p['subtitle']}</p>
        <p class="product-tagline">{p['tagline']}</p>
        <p class="product-desc">{p['description']}</p>
        <div class="keynote-box"><strong>Key Note:</strong> {p['keynote']}</div>
        <div class="contact-box">
            <p>{contact_p}</p>
            <a href="mailto:contact@smyrnaandsable.com">{contact_btn}</a>
        </div>
    </div>"""

    return HTMLResponse(content=render_page(p['name'], body, lang, slug))

@app.get("/health")
async def health():
    visits = db.all()
    total = len(visits)
    blocked = len([v for v in visits if v.get("type") == "bot_blocked"])
    return {"status": "Sovereign Core Active", "total_traffic": total, "bots_blocked": blocked, "timestamp": datetime.datetime.now().isoformat()}
    