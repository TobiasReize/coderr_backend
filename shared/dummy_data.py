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
        UserProfile.objects.create(
            id=dummy_user.id,
            user=dummy_user,
            username=dummy_user.username,
            first_name=dummy_user.first_name,
            last_name=dummy_user.last_name,
            type=types[index],
            email=dummy_user.email
        )

    # Offers erstellen:
    # Offer 1:
    offer_details_list = [
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
    offer_details = [OfferDetail(**item) for item in offer_details_list]
    offer = Offer.objects.create(
        user=User.objects.get(username='hans_lustig'),
        title='Effiziente Backend-Entwicklung',
        description='Ich erstelle ein einfaches, vollständiges Backend für Ihre Anwendung (15-20 APIs).',
    )
    offer.details.set(offer_details, bulk=False)

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
        user=User.objects.get(username='maria_gross'),
        title='Webentwicklung',
        description='Ich führe Frontend-Webentwicklung in Angular und TypeScript durch.',
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
        user=User.objects.get(username='michael_mueller'),
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
        user=User.objects.get(username='business_guest'),
        title='API Integration',
        description='Ich entwickle und integriere fachmännisch APIs um Frontend und Backend nahtlos zu verbinden.',
    )
    offer_4.details.set(offer_details_4, bulk=False)
