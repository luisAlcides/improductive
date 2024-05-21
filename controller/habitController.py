from model.habitModel import HabitModel


class HabitController:
    def __init__(self):
        self.model = HabitModel()

    def insert_into_habits(self, category):
        self.model.insert_into_habits(category)

    def get_category_habits(self):
        return self.model.get_category_habits()

    def was_successful(self):
        return self.model.was_successful()

    def show_monthly_data(self, view):
        data = self.model.fetch_monthly_data()
        if not data:
            view.show_message(
                "No hay datos suficientes para mostrar los datos mensuales."
            )
            return
        view.setup_chart(data, "Monthly Study Time and Goals", "Month", "Hours")

    def show_weekly_data(self, view):
        data = self.model.fetch_weekly_data()
        if not data:
            view.show_message(
                "No hay datos suficientes para mostrar los datos semanales."
            )
            return
        view.setup_chart(data, "Weekly Study Time", "Weeks", "Hours")

    def show_yearly_data(self, view):
        data = self.model.fetch_yearly_data()
        if not data:
            view.show_message(
                "No hay datos suficientes para mostrar los datos anuales."
            )
            return
        view.setup_chart(data, "Yearly Study Time", "Years", "Hours")

    def show_data_by_month(self, month, view):
        data = self.model.fetch_data_by_month(month)
        if not data:
            view.show_message(
                f"No hay datos suficientes para mostrar los datos del mes {month}."
            )
            return
        view.setup_chart(data, f"Study Time for {month}", "Habits", "Hours")
