#
#from wtforms import validators, Form, StringField
#
#class ValidarForm(Form):
#    glasses_type=StringField('nombre', [
#        validators.Required(message= 'El nombre es requerido'),
#        validators.Length(min=1, max=255,message="La longitud debe ser entre 1 y 255 caracteres")
#    ])
#    model_name=StringField('direccion', [
#        validators.Required(message= 'La direccion es requerida'),
#        validators.Length(min=1, max=255,message="La longitud debe ser entre 1 y 255 caracteres")
#    ])
#    description=StringField('coordenadas', [
#        validators.Required(message= 'Las coordenadas son requeridas'),
#        validators.Length(min=1, max=255,message="La longitud debe ser entre 1 y 255 caracteres")
#    ])
#    fecha=StringField('status', [
#        validators.Required(message= 'El estado es requerido'),
#        validators.Length(min=1, max=255,message="La longitud debe ser entre 1 y 255 caracteres")
#    ])