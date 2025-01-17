from models import db, Device

class Microcontroller(db.Model):
    __tablename__ = "microcontrollers"
    id = db.Column("id", db.Integer, db.ForeignKey(Device.id), primary_key=True)
    port = db.Column(db.String(20))

    alert = db.relationship("Alert", backref="microcontroller", lazy=True)

    def get_microcontrollers():
        microcontrollers = Microcontroller.query.join(Device, Device.id == Microcontroller.id)\
                    .add_columns(Microcontroller.id, Device.name, Device.brand, Device.model, 
                                 Device.voltage, Device.description,  Device.is_active, Microcontroller.port).all()
        
        return microcontrollers
    
    def save_microcontroller(name, brand, model, description, voltage, is_active, port):
        device = Device(name=name, brand=brand, model=model, 
                            description=description, voltage=voltage, is_active=is_active)
    
        microcontroller = Microcontroller(id=device.id, port=port)
        
        device.microcontrollers.append(microcontroller)
        db.session.add(device)
        db.session.commit()

    def delete_microcontroller(id):
        try:
            Microcontroller.query.filter_by(id=id).delete()
            Device.query.filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            return False

    def delete_microcontroller_by_port(port):
        Microcontroller.query.filter_by(port=port).delete()
        db.session.commit()

    def update_microcontroller(data):
        Device.query.filter_by(id=data['id'])\
                .update(dict(name=data['name'], brand=data['brand'], model=data['model'], 
                        voltage=data['voltage'], description=data['description'], 
                        is_active=data['is_active']))
        
        Microcontroller.query.filter_by(id=data['id'])\
                        .update(dict(port=data['port']))
        db.session.commit()
