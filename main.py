import flet as ft
import pyrebase

# Firebase Web Config maglumatlaryňyzy bu ýere giriziň
firebaseConfig = {
    "apiKey": "ÖZ_API_KEY_NYZY_ÝAZYN",
    "authDomain": "oz-proyektin.firebaseapp.com",
    "projectId": "oz-proyektin",
    "storageBucket": "oz-proyektin.appspot.com",
    "messagingSenderId": "sende-bar",
    "appId": "1:sende:web:bar"
}

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database() # Realtime Database ýa-da Firestore REST
except Exception as e:
    print("Firebase baglanyşyk ýalňyşlygy:", e)

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

    title_text = ft.Text("ÝOLÝOLDAŞ (Python APK)", size=22, weight=ft.FontWeight.BOLD, color=ACCENT_BLUE)
    
    cities = ["Aşgabat", "Mary", "Lebap", "Daşoguz", "Balkanabat", "Ahal"]
    city_from = ft.Dropdown(label="Nireden", options=[ft.dropdown.Option(c) for c in cities], bgcolor=PANEL_BG)
    city_to = ft.Dropdown(label="Nirä", options=[ft.dropdown.Option(c) for c in cities], bgcolor=PANEL_BG)
    driver_name = ft.TextField(label="Sürüjiniň Ady", bgcolor=PANEL_BG)
    driver_phone = ft.TextField(label="Telefon Belgisi", prefix_text="+993 ", bgcolor=PANEL_BG)
    price_field = ft.TextField(label="Bahasy (TMT)", keyboard_type=ft.KeyboardType.NUMBER, bgcolor=PANEL_BG)
    car_model = ft.TextField(label="Maşyn Modeli", bgcolor=PANEL_BG)

    rides_column = ft.Column()

    def load_rides():
        rides_column.controls.clear()
        try:
            rides = db.child("rides").get()
            if rides.each():
                for ride in rides.each():
                    data = ride.val()
                    card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"{data.get('from')} ➔ {data.get('to')}", weight=ft.FontWeight.BOLD, color=ACCENT_BLUE),
                                ft.Text(f"{data.get('price')} TMT", color=ACCENT_GREEN, weight=ft.FontWeight.BOLD)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Sürüji: {data.get('driver')} | Tel: {data.get('phone')}"),
                            ft.Text(f"Maşyn: {data.get('car', 'Görkezilmän')}", size=12, color=ft.colors.GREY_400),
                        ]),
                        bgcolor=PANEL_BG,
                        padding=15,
                        border_radius=10,
                        margin=ft.margin.symmetric(vertical=5)
                    )
                    rides_column.controls.append(card)
        except Exception as e:
            rides_column.controls.append(ft.Text(f"Maglumat çekmekde ýalňyşlyk: {e}", color=ft.colors.RED))
        page.update()

    def submit_ride(e):
        if not driver_name.value or not driver_phone.value or not price_field.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Ähli meýdançalary dolduryň!"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return

        try:
            data = {
                "driver": driver_name.value,
                "phone": "+993" + driver_phone.value,
                "from": city_from.value,
                "to": city_to.value,
                "price": price_field.value,
                "car": car_model.value
            }
            db.child("rides").push(data)
            page.snack_bar = ft.SnackBar(ft.Text("✅ Yglanyňyz üstünlikli goşuldy!"), bgcolor=ACCENT_GREEN)
            page.snack_bar.open = True
            driver_name.value = ""
            driver_phone.value = ""
            price_field.value = ""
            car_model.value = ""
            load_rides()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ýalňyşlyk: {ex}"), bgcolor=ft.colors.RED_700)
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
                    ft.ElevatedButton("🔄 Täzele", on_click=lambda _: load_rides()),
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
