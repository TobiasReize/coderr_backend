from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from user_auth_app.models import UserProfile
from coderr_app.models import Offer, OfferDetail, Order, Review


def create_dummy_data():
    # User erstellen:
    usernames = ['customer_guest', 'business_guest', 'jannik_schmidt', 'hans_lustig', 'eva_klein', 'maria_gross', 'xaver_steig', 'michael_mueller']
    first_names = ['Customer', 'Business', 'Jannik', 'Hans', 'Eva', 'Maria', 'Xaver', 'Michael']
    last_names = ['Guest', 'Guest', 'Schmidt', 'Lustig', 'Klein', 'Gross', 'Steig', 'Mueller']
    emails = ['customer@guest.de', 'business@guest.de', 'schmidt@user.com', 'hans@test.de', 'eva@dev.com', 'maria@test.de', 'xaver@user.de', 'mueller@test.de']
    passwords = ['asdasd', 'asdasd24', '123456', 'qwertz', '654321', 'test123', '123test', 'asdfgh']
    types = ['customer', 'business', 'customer', 'business', 'customer', 'business', 'customer', 'business']
    locations = ['Würzburg', 'Berlin', 'Hamburg', 'Stuttgart']
    tels = ['0123456789', '9876543210', '0147258369', '9638527410']
    descriptions = [
        'Ich entwickle robuste und skalierbare Backend-Lösungen für Ihre Web-App. Mit Erfahrung in Technologien, z.B. Python und Django optimiere ich Ihre Server-Seite für maximale Leistung und Sicherheit.',
        'Moderne und responsive Frontend-Entwicklung mit HTML, CSS, TS/JS und Angular um visuell ansprechende und funktionale Websites auf allen Geräten zu erstellen. Lass uns deine Idee verwirklichen!',
        'Ich entwickle robuste und skalierbare Fullstack-Lösungen für Ihre Webapplikation. Mit Erfahrungen in z.B. Angular, React JS, Python und Django entwickle ich Ihr individuelles Projekt nach Ihren Vorstellungen.',
        'Die Kommunikation und Anbindung von Frontend und Backend ist meine Leidenschaft. Ganz egal welche API-Technologie Sie verwenden möchten, ich werde sie in Ihr Projekt effizient integrieren.'
    ]
    working_hours = [
        'Bevorzugte Arbeitszeiten: Mi-Fr, 15:00-19:00',
        'Täglich 08:00 - 12:00',
        'Bevorzugte Arbeitszeiten: Mo-Do, 11:00-13:00',
        'Täglich 10:00 - 14:00',
    ]

    for index in [0, 1, 2, 3, 4, 5, 6, 7]:
        dummy_user = User(
            username=usernames[index],
            first_name=first_names[index],
            last_name=last_names[index],
            email=emails[index]
        )
        dummy_user.set_password(passwords[index])
        dummy_user.save()
        Token.objects.get_or_create(user=dummy_user)

        if index % 2 == 0:
            # Customer User:
            UserProfile.objects.create(
                id=dummy_user.id,
                user=dummy_user,
                username=dummy_user.username,
                first_name=dummy_user.first_name,
                last_name=dummy_user.last_name,
                type=types[index],
                email=dummy_user.email
            )
        else:
            # Business User:
            UserProfile.objects.create(
                id=dummy_user.id,
                user=dummy_user,
                username=dummy_user.username,
                first_name=dummy_user.first_name,
                last_name=dummy_user.last_name,
                type=types[index],
                email=dummy_user.email,
                location=locations[index],
                tel=tels[index],
                description=descriptions[index],
                working_hours=working_hours[index],
            )

    # Offers erstellen:
    # Offer 1:
    offer_details_list_1 = [
        {
            'title': 'Basic Development',
            'revisions': 5,
            'delivery_time_in_days': 10,
            'price': 112.44,
            'features': ['API-Integration', 'Datenbank-Setup', 'Sicherheitsmaßnahmen'],
            'offer_type': 'basic'
        },
        {
            'title': 'Standard Development',
            'revisions': 10,
            'delivery_time_in_days': 12,
            'price': 222.44,
            'features': ['API-Integration', 'Datenbank-Setup', 'Sicherheitsmaßnahmen'],
            'offer_type': 'standard'
        },
        {
            'title': 'Premium Development',
            'revisions': -1,
            'delivery_time_in_days': 12,
            'price': 454.99,
            'features': ['API-Integration', 'Datenbank-Setup', 'Sicherheitsmaßnahmen'],
            'offer_type': 'premium'
        }
    ]
    offer_details_1 = [OfferDetail(**item) for item in offer_details_list_1]
    offer_1 = Offer.objects.create(
        user=User.objects.get(username='business_guest'),
        title='Effiziente Backend-Entwicklung',
        description='Ich erstelle ein einfaches, vollständiges Backend für Ihre Anwendung (15-20 APIs).',
    )
    offer_1.details.set(offer_details_1, bulk=False)

    # Offer 2:
    offer_details_list_2 = [
        {
            'title': 'Basic Webentwicklung',
            'revisions': 4,
            'delivery_time_in_days': 6,
            'price': 99.99,
            'features': ['Einfache Landing-Page'],
            'offer_type': 'basic'
        },
        {
            'title': 'Standard Webentwicklung',
            'revisions': 10,
            'delivery_time_in_days': 11,
            'price': 133.89,
            'features': ['Landing-Page inkl. Subpages', 'Responsive Design'],
            'offer_type': 'standard'
        },
        {
            'title': 'Premium Webentwicklung',
            'revisions': -1,
            'delivery_time_in_days': 14,
            'price': 255.99,
            'features': ['Komplette Webapplikation', 'Responsive Design', 'Skalierbarkeit'],
            'offer_type': 'premium'
        }
    ]
    offer_details_2 = [OfferDetail(**item) for item in offer_details_list_2]
    offer_2 = Offer.objects.create(
        user=User.objects.get(username='hans_lustig'),
        title='Webentwicklung',
        description='Ich führe Frontend-Webentwicklung in Angular und TypeScript/JavaScript durch.',
    )
    offer_2.details.set(offer_details_2, bulk=False)

    # Offer 3:
    offer_details_list_3 = [
        {
            'title': 'Basic Paket',
            'revisions': 6,
            'delivery_time_in_days': 7,
            'price': 199.99,
            'features': ['Einfache Webanwendung'],
            'offer_type': 'basic'
        },
        {
            'title': 'Standard Paket',
            'revisions': 10,
            'delivery_time_in_days': 12,
            'price': 233.89,
            'features': ['Einfache Webanwendung', 'Fertige Backendlösung', 'Skalierbarkeit'],
            'offer_type': 'standard'
        },
        {
            'title': 'Premium Paket',
            'revisions': -1,
            'delivery_time_in_days': 16,
            'price': 555.99,
            'features': ['Komplexe Webapplikation', 'Individuelle Backendlösung', 'Sicherheitsmaßnahmen', 'Skalierbarkeit'],
            'offer_type': 'premium'
        }
    ]
    offer_details_3 = [OfferDetail(**item) for item in offer_details_list_3]
    offer_3 = Offer.objects.create(
        user=User.objects.get(username='maria_gross'),
        title='Fullstack Development',
        description='Ich entwickle Frontend-, Backend- oder Fullstack-Lösungen nach Ihren Vorstellungen.',
    )
    offer_3.details.set(offer_details_3, bulk=False)

    # Offer 4:
    offer_details_list_4 = [
        {
            'title': 'Einfache API Integration',
            'revisions': 7,
            'delivery_time_in_days': 7,
            'price': 99.99,
            'features': ['Fertige API Integration'],
            'offer_type': 'basic'
        },
        {
            'title': 'Standard API Integration',
            'revisions': 10,
            'delivery_time_in_days': 13,
            'price': 133.89,
            'features': ['Fertige API Integration', 'Skalierbarkeit', 'Frontend Integration'],
            'offer_type': 'standard'
        },
        {
            'title': '20 Endpoints',
            'revisions': -1,
            'delivery_time_in_days': 16,
            'price': 324.99,
            'features': ['Individuelle API-Entwicklung', 'Individuelle Frontend Integration', 'Sicherheitsmaßnahmen', 'Skalierbarkeit'],
            'offer_type': 'premium'
        }
    ]
    offer_details_4 = [OfferDetail(**item) for item in offer_details_list_4]
    offer_4 = Offer.objects.create(
        user=User.objects.get(username='michael_mueller'),
        title='API Integration',
        description='Ich entwickle und integriere fachmännisch APIs um Frontend und Backend nahtlos zu verbinden.',
    )
    offer_4.details.set(offer_details_4, bulk=False)

    # Orders erstellen:
    # Order 1:
    offer_detail_1 = OfferDetail.objects.get(id=5)
    order_1 = Order.objects.create(
        offer_detail=offer_detail_1,
        customer_user=User.objects.get(username='customer_guest'),
        business_user=offer_detail_1.offer.user,
        status='completed'
    )
    
    # Order 2:
    offer_detail_2 = OfferDetail.objects.get(id=6)
    order_2 = Order.objects.create(
        offer_detail=offer_detail_2,
        customer_user=User.objects.get(username='customer_guest'),
        business_user=offer_detail_2.offer.user,
        status='in_progress'
    )
    
    # Order 3:
    offer_detail_3 = OfferDetail.objects.get(id=1)
    order_3 = Order.objects.create(
        offer_detail=offer_detail_3,
        customer_user=User.objects.get(username='jannik_schmidt'),
        business_user=offer_detail_3.offer.user,
        status='cancelled'
    )
    
    # Order 4:
    offer_detail_4 = OfferDetail.objects.get(id=4)
    order_4 = Order.objects.create(
        offer_detail=offer_detail_4,
        customer_user=User.objects.get(username='eva_klein'),
        business_user=offer_detail_4.offer.user,
        status='in_progress'
    )
    
    # Order 5:
    offer_detail_5 = OfferDetail.objects.get(id=11)
    order_5 = Order.objects.create(
        offer_detail=offer_detail_5,
        customer_user=User.objects.get(username='xaver_steig'),
        business_user=offer_detail_5.offer.user,
        status='completed'
    )
    
    # Order 6:
    offer_detail_6 = OfferDetail.objects.get(id=9)
    order_6 = Order.objects.create(
        offer_detail=offer_detail_6,
        customer_user=User.objects.get(username='xaver_steig'),
        business_user=offer_detail_6.offer.user,
        status='in_progress'
    )

    # Reviews erstellen:
    # Review 1:
    Review.objects.create(
        business_user=order_1.business_user,
        reviewer=order_1.customer_user,
        rating=4,
        description='Schnelle und professionelle Arbeit. Das Design ist modern und funktioniert perfekt auf allen Geräten!',
    )
    
    # Review 2:
    Review.objects.create(
        business_user=order_2.business_user,
        reviewer=order_2.customer_user,
        rating=5,
        description='Sehr zufrieden mit dem Ergebnis - kreatives Design, schnelle Umsetzung, jederzeit gerne wieder!',
    )
    
    # Review 3:
    Review.objects.create(
        business_user=order_3.business_user,
        reviewer=order_3.customer_user,
        rating=3,
        description='Nach dem ersten Release wies das Backend noch einige Optimierungsmöglichkeiten auf. Funktioniert aber trotzdem gut!',
    )
    
    # Review 4:
    Review.objects.create(
        business_user=order_4.business_user,
        reviewer=order_4.customer_user,
        rating=4,
        description='Kreative und ansprechende Landing-Page. Sehr zufrieden mit der Umsetzung!',
    )
    
    # Review 5:
    Review.objects.create(
        business_user=order_5.business_user,
        reviewer=order_5.customer_user,
        rating=4,
        description='Tolle Zusammenarbeit! Gelungenes Ergebnis. Gerne wieder :)',
    )
    
    # Review 6:
    Review.objects.create(
        business_user=order_6.business_user,
        reviewer=order_6.customer_user,
        rating=3,
        description='Hatte für das Ergebnis etwas mehr erwartet. Anwendung läuft trotzdem stabil und fehlerfrei!',
    )
