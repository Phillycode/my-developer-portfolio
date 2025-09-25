from django.core.mail import EmailMessage
from decimal import Decimal


class EmailBuilder:

    @staticmethod
    def build_pw_reset_email(user, reset_url):
        subject = "Password Reset"
        user_email = user.email
        domain_email = "help@evermarket.com"
        body = (
            f"Hi {user.username},\nHere is your link to reset your "
            f"password: {reset_url}"
        )
        email = EmailMessage(subject, body, domain_email, [user_email])
        return email

    @staticmethod
    def build_invoice_email(user, cart):
        subject = "Invoice from Evermarket"
        user_email = user.email
        domain_email = "sales@evermarket.com"
        body_intro = (
            f"Hi {user.username},\nThank you for your purchase!"
            "\nPlease find the details of your purchase below:\n"
        )

        if not cart:
            body_main = ["No items found in cart."]
            total = 0
        else:
            body_main = []
            total = 0
            # Loop through dictionary values
            for item in cart.values():
                qty = item["quantity"]
                price = Decimal(item["price"])
                line_total = qty * price
                body_main.append(
                    f"{qty} x {item['name']} @ R{price} - R{line_total}"
                )
                total += line_total

        body_end = (
            f"\nTotal: R{total}\n"
            "\nIf you require further assistance with your order, "
            "don't hesitate to contact us at help@evermarket.com.\n"
            "We hope to see you again!"
        )

        body = f"{body_intro}\n" + "\n".join(body_main) + body_end
        email = EmailMessage(subject, body, domain_email, [user_email])
        return email
