# Copyright (c) 2026, Rainier Jombreini Polanco Estrella. and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

TEMPLATE_PATH = "/home/frappe/frappe-bench/apps/print_master/print_master/templates"

class PrintMasterTemplate(Document):
	
	def validate(self):
		self.set_path_field()

	def set_path_field(self, TEMPLATE_PATH=TEMPLATE_PATH):
		#si el campo de template_path esta vacio, se asigna el valor del campo template_name y se crea un modulo en la ruta especificada
		if not self.template_path:
			self.template_path = f"{TEMPLATE_PATH}/{self.template_name}.html"
			#crear el archivo en la ruta especificada
			with open(self.template_path, "w") as f:
				f.write(f"<!-- Template: {self.template_name} -->\n")
				f.write("<html>\n")
				f.write("<head>\n")
				f.write(f"<title>{self.template_name}</title>\n")
				f.write("</head>\n")
				f.write("<body>\n")
				f.write(f"<h1>{self.template_name}</h1>\n")
				f.write("<!-- Add your template content here -->\n")
				f.write("</body>\n")
				f.write("</html>\n")


def get_context(is_a_template=True, doc=None, config=None):
    if is_a_template:
        # Intentamos obtener la factura más reciente para usar data real como ejemplo
        # Si no hay facturas, creamos un documento vacío del tipo Sales Invoice
        sample_doc_name = frappe.db.get_value("Sales Invoice", {}, "name", order_by="creation desc")
        
        if sample_doc_name:
            doc = frappe.get_doc("Sales Invoice", sample_doc_name)
        else:
            # Si el sitio está vacío, creamos un doc virtual para que no falle .get_formatted
            doc = frappe.new_doc("Sales Invoice")
            doc.name = "INV-2026-001"
            doc.customer_name = "Cliente de Ejemplo RPDEV"
            doc.posting_date = frappe.utils.nowdate()
            doc.append("items", {"item_name": "Servicio MVP", "qty": 1, "rate": 1000, "amount": 1000})

        return {
            "doc": doc,
            "config": config or frappe._dict({
                "primary_color": "#1e4ea1",
                "font_family": "Arial",
                "logo": "/private/files/Gemini_Generated_Image_amyizlamyizlamyi - Editado.png"
            })
        }
    else:
        return {
            "doc": doc,
            "config": config
        }

# @frappe.whitelist()
# def get_template_preview(template_name, doc=None, config=None):
# 	doc = frappe.get_doc("Print Master Template", template_name)
# 	if doc.template_path:
# 		html = frappe.render_template(
# 			open(doc.template_path, "r").read(),
# 			get_context(is_a_template=True, doc=doc, config=config)
# 		)
# 		return html
# 	# 	with open(doc.template_path, "r") as f:
# 	# 		# frappe.errprint(f"Reading template from: {f.read()}")
# 	# 		return f.read()
# 	# return "No hay contenido para mostrar."


@frappe.whitelist()
def get_template_preview(template_name, doc=None, config=None):
    # Si config viene como string (desde JS), lo convertimos a diccionario
    if isinstance(config, str):
        config = json.loads(config)
    
    config_dict = frappe._dict(config or {})
    
    doc_template = frappe.get_doc("Print Master Template", template_name)
    
    if doc_template.template_path:
        with open(doc_template.template_path, "r") as f:
            source_html = f.read()
            
        # Obtenemos el contexto (is_a_template=True para usar data de ejemplo)
        context = get_context(is_a_template=True, config=config_dict)
        context.update(frappe.utils.get_jinja_helper())
        
        return frappe.render_template(source_html, context)