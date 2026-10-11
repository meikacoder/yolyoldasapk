import flet as ft
import requests
import json

PROJECT_ID = "tkmtaxi-a99f4"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{tkmtaxi-a99f4}/databases/(default)/documents/rides"
USERS_URL = f"https://firestore.googleapis.com/v1/projects/{tkmtaxi-a99f4}/databases/(default)/documents/users"

def main(page: ft.Page):
    page.title = "Ýolýoldaş — Şäherara Taksiler"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    # Web sahypaňdaky dizaýn reňkleri we stilleri
    BG_MAIN = "#0B0F19"
    PANEL_BG = "#151D2A"
    CARD_BG = "#1E293B"
    ACCENT_GREEN = "#00E676"
    ACCENT_BLUE = "#00E5FF"
    ACCENT_GOLD = "#FFD700"
    TEXT_MUTED = "#94A3B8"
    ADMIN_PASS = "20+90ye12m"

    page.bgcolor = BG_MAIN

    title_text = ft.Text("🚗 Ýolýoldaş", size=24, weight=ft.FontWeight.BOLD, color=ACCENT_BLUE)
    subtitle_text = ft.Text("Türkmenistanyň şäherara ugurlary boýunça amatly we ynamly platforma", size=12, color=TEXT_MUTED)

    cities = ["Aşgabat", "Mary", "Lebap", "Daşoguz", "Balkanabat", "Ahal"]
    
    city_from = ft.Dropdown(
        label="📍 Nireden", 
        options=[ft.dropdown.Option(c) for c in cities], 
        bgcolor=PANEL_BG,
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN
    )
    city_to = ft.Dropdown(
        label="🎯 Nirä", 
        options=[ft.dropdown.Option(c) for c in cities], 
        bgcolor=PANEL_BG,
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN
    )
    driver_name = ft.TextField(
        label="👤 Sürüjiniň Ady", 
        bgcolor=PANEL_BG, 
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN
    )
    driver_phone = ft.TextField(
        label="📞 Telefon Belgisi", 
        prefix_text="+993 ", 
        bgcolor=PANEL_BG, 
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN,
        keyboard_type=ft.KeyboardType.PHONE
    )
    ride_time = ft.TextField(
        label="📅 Gidiljek Wagty",
        hint_text="YYYY-MM-DD HH:MM",
        bgcolor=PANEL_BG,
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN
    )
    price_field = ft.TextField(
        label="💰 1 Orun Bahasy (TMT)", 
        keyboard_type=ft.KeyboardType.NUMBER, 
        bgcolor=PANEL_BG, 
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN
    )
    car_model = ft.TextField(
        label="🚙 Maşyn Modeli", 
        bgcolor=PANEL_BG, 
        border_color=ACCENT_BLUE,
        focused_border_color=ACCENT_GREEN
    )

    rides_column = ft.Column()

    def load_rides(e=None):
        rides_column.controls.clear()
        try:
            response = requests.get(FIRESTORE_URL)
            if response.status_code == 200:
                data = response.json()
                documents = data.get("documents", [])
                
                if not documents:
                    rides_column.controls.append(
                        ft.Container(
                            content=ft.Text("⚠️ Yglan tapylmady.", color=TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                            padding=20
                        )
                    )
                    page.update()
                    return

                rides_list = []
                for doc in documents:
                    fields = doc.get("fields", {})
                    # Firestore REST formatyndan okamak
                    name_parts = doc.get("name", "").split("/")
                    doc_id = name_parts[-1] if name_parts else ""
                    
                    drv = fields.get("driver", {}).get("stringValue", "Näbelli")
                    phn = fields.get("phone", {}).get("stringValue", "")
                    frm = fields.get("from", {}).get("stringValue", "")
                    to_ = fields.get("to", {}).get("stringValue", "")
                    prc = fields.get("price", {}).get("stringValue", "0")
                    car = fields.get("car", {}).get("stringValue", "-")
                    time_val = fields.get("time", {}).get("stringValue", "")
                    is_pro = fields.get("isProDriver", {}).get("booleanValue", False)

                    rides_list.append({
                        "id": doc_id,
                        "driver": drv,
                        "phone": phn,
                        "from": frm,
                        "to": to_,
                        "price": prc,
                        "car": car,
                        "time": time_val,
                        "isProDriver": is_pro
                    })

                # PRO yglanlary öňe çykarmak sort logika
                rides_list.sort(key=lambda x: x["isProDriver"], reverse=True)

                for ride in rides_list:
                    card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"{ride['from']} ➔ {ride['to']}", weight=ft.FontWeight.BOLD, size=16, color=ACCENT_BLUE),
                                ft.Container(
                                    content=ft.Text(f"{ride['price']} TMT", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                                    bgcolor=ACCENT_GREEN,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=6
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(height=10, color=ft.colors.WHITE10),
                            ft.Row([
                                ft.Icon(ft.icons.PERSON, size=16, color=TEXT_MUTED),
                                ft.Text(f"Sürüji: {ride['driver']}", color=ft.colors.WHITE),
                                ft.Container(content=ft.Text("⭐ VIP" if ride['isProDriver'] else "", color=ACCENT_GOLD, size=11, weight=ft.FontWeight.BOLD))
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.PHONE, size=16, color=TEXT_MUTED),
                                ft.Text(f"Tel: {ride['phone']}", color=ft.colors.WHITE),
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.DIRECTIONS_CAR, size=16, color=TEXT_MUTED),
                                ft.Text(f"Maşyn: {ride['car']} | Wagty: {ride['time']}", size=13, color=TEXT_MUTED),
                            ]),
                        ]),
                        bgcolor=CARD_BG,
                        padding=15,
                        border_radius=12,
                        margin=ft.margin.symmetric(vertical=6),
                        border=ft.border.all(2, ACCENT_GOLD if ride['isProDriver'] else ft.colors.WHITE10)
                    )
                    rides_column.controls.append(card)
            else:
                rides_column.controls.append(ft.Text("Maglumat alyp bolmady.", color=ft.colors.RED_400))
        except Exception as ex:
            rides_column.controls.append(ft.Text(f"Ýalňyşlyk: {ex}", color=ft.colors.RED_400))
        page.update()

    def submit_ride(e):
        if not driver_name.value or not driver_phone.value or not price_field.value or not city_from.value or not city_to.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Ähli meýdançalary doly dolduryň!"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return

        try:
            payload = {
                "fields": {
                    "driver": {"stringValue": driver_name.value},
                    "phone": {"stringValue": "+993" + driver_phone.value},
                    "from": {"stringValue": city_from.value},
                    "to": {"stringValue": city_to.value},
                    "price": {"stringValue": price_field.value},
                    "car": {"stringValue": car_model.value if car_model.value else "-"},
                    "time": {"stringValue": ride_time.value if ride_time.value else ""},
                    "isProDriver": {"booleanValue": False} # Deslapky
                }
            }
            
            response = requests.post(FIRESTORE_URL, json=payload)
            if response.status_code in [200, 201]:
                page.snack_bar = ft.SnackBar(ft.Text("✅ Yglanyňyz üstünlikli goşuldy! Saýtdada görünýär."), bgcolor=ACCENT_GREEN)
                page.snack_bar.open = True
                driver_name.value = ""
                driver_phone.value = ""
                price_field.value = ""
                car_model.value = ""
                ride_time.value = ""
                city_from.value = None
                city_to.value = None
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
        width=300,
        height=45
    )

    # PRO Sürüji Dialog Penjiresi
    def open_pro_dlg(e):
        def select_plan(plan_name, price, days):
            page.dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"💳 Töleg: {price} TMT. +99364410621 belgä iberiň!"), bgcolor=ACCENT_GOLD)
            page.snack_bar.open = True
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("⭐ PRO Sürüji Meýilnamalary", color=ACCENT_GOLD),
            content=ft.Column([
                ft.Text("Yglanlaryňyzy hemmeleriň ýokarsynda we VIP belligi bilen görkeziň!"),
                ft.ElevatedButton("Standard (3 gün) - 5 TMT", on_click=lambda _: select_plan("standard", 5, 3), bgcolor=PANEL_BG, color=ACCENT_GREEN),
                ft.ElevatedButton("Premium (10 gün) - 10 TMT", on_click=lambda _: select_plan("premium", 10, 10), bgcolor=PANEL_BG, color=ACCENT_GREEN),
                ft.ElevatedButton("PRO User (1 aý) - 20 TMT", on_click=lambda _: select_plan("pro", 20, 30), bgcolor=PANEL_BG, color=ACCENT_GREEN),
            ], height=200, tight=True),
            actions=[ft.TextButton("Ýapmak", on_click=lambda _: setattr(page.dialog, 'open', False) or page.update())]
        )
        page.dialog.open = True
        page.update()

    pro_btn = ft.ElevatedButton("⭐ PRO Agzalyk", on_click=open_pro_dlg, bgcolor=ACCENT_GOLD, color=ft.colors.BLACK)

    # Admin Panel Dialog
    def open_admin_dlg(e):
        passw_input = ft.TextField(label="Admin Paroly", password=True, can_reveal_password=True, border_color=ACCENT_BLUE)

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

    admin_btn = ft.TextButton("🔑 Admin", on_click=open_admin_dlg, icon=ft.icons.ADMIN_PANEL_SETTINGS)

    # Esasy Tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Taxiler",
                content=ft.Column([
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.Row([
                        ft.ElevatedButton("🔄 Täzele", on_click=load_rides, bgcolor=PANEL_BG, color=ACCENT_BLUE),
                        pro_btn
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    rides_column
                ], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Tab(
                text="➕ Taksi Goş",
                content=ft.Column([
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    city_from, city_to, driver_name, driver_phone, ride_time, price_field, car_model,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    submit_btn
                ], scroll=ft.ScrollMode.AUTO)
            )
        ]
    )

    page.add(
        ft.Row([
            ft.Column([title_text, subtitle_text]), 
            admin_btn
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=15, color=ft.colors.WHITE10),
        tabs
    )
    
    load_rides()
ft.app(target=main)
