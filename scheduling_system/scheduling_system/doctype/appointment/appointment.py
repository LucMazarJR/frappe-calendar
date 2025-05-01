# Copyright (c) 2025, Nexforce and contributors
# For license information, please see license.txt

from frappe.model.document import Document # type: ignore
import frappe # type: ignore
from frappe.utils import get_datetime, add_to_date # type: ignore

class Appointment(Document):
    def before_save(self):
        # 1. Calcular end_date a partir da duração
        if self.duration and self.start_date:
            try:
                duration_parts = self.duration.split(":")
                hours = int(duration_parts[0])
                minutes = int(duration_parts[1]) if len(duration_parts) > 1 else 0
            except:
                frappe.throw("Invalid date format")

            start_datetime = get_datetime(self.start_date)
            self.end_date = add_to_date(
                start_datetime,
                hours=hours,
                minutes=minutes,
                as_string=True
            )
            self.end_date = get_datetime(self.end_date).strftime("%Y-%m-%d %H:%M")

        # 2. Validar ordem das datas
        if get_datetime(self.start_date) >= get_datetime(self.end_date):
            frappe.throw("The start date must be before the end date")

        # 3. Verificar conflitos de agendamento
        overlapping_appointments = frappe.get_all(
            'Appointment',
            filters={
                'seller': self.seller,
                'status': 'Scheduled',
                'start_date': ['<', self.end_date],
                'end_date': ['>', self.start_date],
                'name': ['!=', self.name]
            },
            fields=['name', 'start_date', 'end_date']
        )

        if overlapping_appointments:
            conflict_list = "\n".join(
                [f"- {app.start_date} → {app.end_date} (ID: {app.name})"
                for app in overlapping_appointments]
            )
            frappe.throw(
                f"The seller {self.seller} already have appointments scheduled:<br>{conflict_list}",
                title="Schedule conflict"
            )