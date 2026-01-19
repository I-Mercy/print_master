// Copyright (c) 2026, Rainier Jombreini Polanco Estrella. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Print Master Template", {
    refresh: function(frm) {
        console.log("Refrescando la vista previa del template...");
        frm.trigger('render_preview');
    },
    // Cada vez que guardes, refrescamos la vista
    after_save: function(frm) {
        frm.trigger('render_preview');
    },
    render_preview: function(frm) {
        frappe.call({
            method: "print_master.print_master.doctype.print_master_template.print_master_template.get_template_preview",
            args: {
                template_name: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    // Seteamos el HTML en tu campo (supongamos que se llama 'preview_html')
                    console.log(`hola ${r.message}`);
                    frm.set_df_property('template', 'options', r.message);
                    frm.refresh_field('template');
                }
            }
        });
    }
});
