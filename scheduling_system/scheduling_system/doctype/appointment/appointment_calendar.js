frappe.views.calendar['Appointment'] = {
    field_map: {
      start: 'start_date',
      end: 'end_date',
      id: 'name',
      allDay: '', 
      title: 'client_name'
    },

    style_map: {
      Scheduled: 'info',   
      Finished: 'success',
      Canceled: 'danger'
    },
    order_by: 'end_date', 
  };