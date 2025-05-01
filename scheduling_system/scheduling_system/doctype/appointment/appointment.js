// Copyright (c) 2025, Nexforce and contributors
// For license information, please see license.txt

frappe.ui.form.on('Appointment', {
    duration: function(frm) {
        if(frm.doc.duration && frm.doc.duration.length > 5) {
            frm.set_value('duration', frm.doc.duration.substring(0, 5));
        }
    }
});