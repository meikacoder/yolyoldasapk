import flet as ft
import requests
import json

# Firebase Firestore Project ID (Saýtyňdaky Firebase proýekt ady)
PROJECT_ID = "tkmtaxi-a99f4"  # Eger üýtgeşik bolsa şuny üýtgedersiňiz
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/tkmtaxi-a99f4}/databases/(default)/documents/rides"

def main(page: ft.Page):
    page.title = "Ýolýoldaş — Şäherara Taksi"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    BG_MAIN = "#0B0F19"
    PANEL_BG = "#151D2A"
    ACCENT_BLUE = "#00E5FF"
    ACCENT_GREEN = "#00E676"
    ADMIN_PASS = "20+90ye12m"

    page.bgcolor = BG_MAIN

    title_text = ft.Text("ÝOLÝOLDAŞ (Synced)", size=22, weight=ft.FontWeight.BOLD, color=ACCENT_BLUE)
    
    cities = ["Aşgabat", "Mary", "Lebap", "Daşoguz", "Balkanabat", "Ahal"]
    city_from = ft.Dropdown(label="Nireden", options=[ft.dropdown.Option(c) for c in cities], bgcolor=PANEL_BG)
    city_to = ft.Dropdown(label="Nirä", options=[ft.dropdown.Option(c) for c in cities], bgcolor=PANEL_BG)
    driver_name = ft.TextField(label="Sürüjiniň Ady", bgcolor=PANEL_BG)
    driver_phone = ft.TextField(label="Telefon Belgisi", prefix_text="+993 ", bgcolor=PANEL_BG)
    price_field = ft.TextField(label="Bahasy (TMT)", keyboard_type=ft.KeyboardType.NUMBER, bgcolor=PANEL_BG)
    car_model = ft.TextField(label="Maşyn Modeli", bgcolor=PANEL_BG)

    rides_column = ft.Column()

    def load_rides(e=None):
        rides_column.controls.clear()
        try:
            response = requests.get(FIRESTORE_URL)
            if response.status_code == 200:
                data = response.json()
                documents = data.get("documents", [])
                
                if not documents:
                    rides_column.controls.append(ft.Text("Häzirlikçe yglan ýok.", color=ft.colors.GREY_400))
                
                for doc in documents:
                    fields = doc.get("fields", {})
                    # Firestore REST formatyndan maglumatlary okamak
                    drv = fields.get("driver", {}).get("stringValue", "Näbelli")
                    phn = fields.get("phone", {}).get("stringValue", "")
                    frm = fields.get("from", {}).get("stringValue", "")
                    to_ = fields.get("to", {}).get("stringValue", "")
                    prc = fields.get("price", {}).get("stringValue", "0")
                    car = fields.get("car", {}).get("stringValue", "-")

                    card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"{frm} ➔ {to_}", weight=ft.FontWeight.BOLD, color=ACCENT_BLUE),
                                ft.Text(f"{prc} TMT", color=ACCENT_GREEN, weight=ft.FontWeight.BOLD)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Sürüji: {drv} | Tel: {phn}"),
                            ft.Text(f"Maşyn: {car}", size=12, color=ft.colors.GREY_400),
                        ]),
                        bgcolor=PANEL_BG,
                        padding=15,
                        border_radius=10,
                        margin=ft.margin.symmetric(vertical=5)
                    )
                    rides_column.controls.append(card)
            else:
                rides_column.controls.append(ft.Text("Maglumat alyp bolmady.", color=ft.colors.RED))
        except Exception as ex:
            rides_column.controls.append(ft.Text(f"Ýalňyşlyk: {ex}", color=ft.colors.RED))
        page.update()

    def submit_ride(e):
        if not driver_name.value or not driver_phone.value or not price_field.value or not city_from.value or not city_to.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Ähli meýdançalary dolduryň!"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Firestore REST formatyna görä maglumat düzmek
            payload = {
                "fields": {
                    "driver": {"stringValue": driver_name.value},
                    "phone": {"stringValue": "+993" + driver_phone.value},
                    "from": {"stringValue": city_from.value},
                    "to": {"stringValue": city_to.value},
                    "price": {"stringValue": price_field.value},
                    "car": {"stringValue": car_model.value if car_model.value else "-"}
                }
            }
            
            response = requests.post(FIRESTORE_URL, json=payload)
            if response.status_code in [200, 201]:
                page.snack_bar = ft.SnackBar(ft.Text("✅ Yglanyňyz üstünlikli goşuldy!"), bgcolor=ACCENT_GREEN)
                page.snack_bar.open = True
                driver_name.value = ""
                driver_phone.value = ""
                price_field.value = ""
                car_model.value = ""
                load_rides()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Ýalňyşlyk ýüze çykdy."), bgcolor=ft.colors.RED_700)
                page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Baglanyşyk ýalňyşlygy: {ex}"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
        page.update()

    submit_btn = ft.ElevatedButton(
        text="📢 Yglany Ýaýratmak",
        color=ft.colors.BLACK,
        bgcolor=ACCENT_GREEN,
        on_click=submit_ride,
        width=300
    )

    def open_admin_dlg(e):
        passw_input = ft.TextField(label="Admin Paroly", password=True, can_reveal_password=True)

        def check_pass(evt):
            if passw_input.value == ADMIN_PASS:
                page.dialog.open = False
                page.snack_bar = ft.SnackBar(ft.Text("🔓 Admin Paneline Girdiňiz!"), bgcolor=ACCENT_GREEN)
                page.snack_bar.open = True
                page.update()
            else:
                passw_input.error_text = "Ýalňyş parol!"
                page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Admin Girişi"),
            content=passw_input,
            actions=[ft.TextButton("Girmek", on_click=check_pass)]
        )
        page.dialog.open = True
        page.update()

    admin_btn = ft.TextButton("🔑 Admin Panel", on_click=open_admin_dlg, icon=ft.icons.ADMIN_PANEL_SETTINGS)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Taxiler",
                content=ft.Column([
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton("🔄 Täzele", on_click=load_rides),
                    rides_column
                ])
            ),
            ft.Tab(
                text="➕ Taxi Goş",
                content=ft.Column([
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    city_from, city_to, driver_name, driver_phone, price_field, car_model,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    submit_btn
                ])
            )
        ]
    )

    page.add(
        ft.Row([title_text, admin_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        tabs
    )
    
    load_rides()

ft.app(target=main)
