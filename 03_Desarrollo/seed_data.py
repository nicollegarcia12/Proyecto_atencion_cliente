import os
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    # Seed Agentes if empty
    if db.query(models.UsuarioAgente).count() == 0:
        print("Seeding initial agents...")
        agentes = [
            models.UsuarioAgente(nombre_completo="Andrés Gómez", correo_electronico="andres.gomez@empresa.com", rol="Agente"),
            models.UsuarioAgente(nombre_completo="Laura Gómez", correo_electronico="laura.gomez@empresa.com", rol="Agente"),
            models.UsuarioAgente(nombre_completo="Miguel Rojas", correo_electronico="miguel.rojas@empresa.com", rol="Administrador")
        ]
        db.add_all(agentes)
        db.commit()

    # Seed Clientes if empty
    if db.query(models.Cliente).count() == 0:
        print("Seeding initial clients...")
        clientes = [
            models.Cliente(nombre_completo="María Fernández", correo_electronico="maria.fernandez@empresa.com", telefono="+573001234567", empresa_organizacion="Tech Solutions S.A.S."),
            models.Cliente(nombre_completo="Carlos Mendoza", correo_electronico="carlos.mendoza@empresa.com", telefono="+573159876543", empresa_organizacion="Innovación Digital")
        ]
        db.add_all(clientes)
        db.commit()

    # Seed Soluciones Knowledge Base if empty
    if db.query(models.Solucion).count() == 0:
        print("Seeding initial knowledge base solutions...")
        admin = db.query(models.UsuarioAgente).filter_by(rol="Administrador").first()
        soluciones = [
            models.Solucion(
                titulo="Procedimiento para desapropiar bloqueos de sesión e inicio de sesión",
                contenido_solucion="Para resolver problemas de inicio de sesión o bloqueo de sesión: 1. Limpie las cookies del navegador. 2. Ingrese a la plataforma e intente restablecer la contraseña desde el enlace de recuperación. 3. Si el problema persiste, contacte a soporte para reiniciar los tokens de acceso.",
                categoria="Acceso y Cuentas",
                palabras_clave="login, acceso, contraseña, clave, bloqueo, sesion",
                id_autor=admin.id_agente if admin else 1
            ),
            models.Solucion(
                titulo="Resolución de caídas de conexión y Timeouts de servidor",
                contenido_solucion="Ante un error de timeout de conexión (HTTP 504 / 500): 1. Verifique su conexión de red local. 2. Realice un test de ping al servidor principal. 3. El equipo técnico ha actualizado las reglas de firewall para garantizar el flujo de datos.",
                categoria="Conectividad y Servidores",
                palabras_clave="timeout, servidor, caido, caído, red, conexion, puerto",
                id_autor=admin.id_agente if admin else 1
            ),
            models.Solucion(
                titulo="Procedimiento de verificación de facturas y pagos",
                contenido_solucion="Las solicitudes de aclaración de cobros o facturación se revisan cruzando los estados de cuenta con la base comercial.",
                categoria="Facturación y Pagos",
                palabras_clave="factura, cobro, pago, saldo, valor",
                id_autor=admin.id_agente if admin else 1
            )
        ]
        db.add_all(soluciones)
        db.commit()

    # Seed Initial Demo Tickets if empty
    if db.query(models.Ticket).count() == 0:
        print("Seeding initial tickets...")
        cliente1 = db.query(models.Cliente).first()
        agente1 = db.query(models.UsuarioAgente).filter_by(rol="Agente").first()

        t1 = models.Ticket(
            codigo_seguimiento="TCK-2026-1001",
            id_cliente=cliente1.id_cliente if cliente1 else 1,
            titulo="Error crítico de acceso y timeout en el portal",
            descripcion="Desde esta mañana no puedo ingresar al sistema, me sale un mensaje de timeout de conexión de forma repetida.",
            categoria_preliminar="Conectividad y Servidores",
            prioridad="Alta",
            estado="Abierto",
            id_agente_asignado=agente1.id_agente if agente1 else 1
        )
        db.add(t1)
        db.commit()
        db.refresh(t1)

        sug1 = models.SugerenciaIA(
            id_ticket=t1.id_ticket,
            prioridad_sugerida="Alta",
            categoria_sugerida="Conectividad y Servidores",
            respuesta_sugerida="Estimado usuario, de acuerdo con nuestra base de conocimiento, este error de timeout suele solucionarse limpiando la caché del navegador o verificando la conectividad de red local.",
            score_confianza=0.95
        )
        db.add(sug1)

        t2 = models.Ticket(
            codigo_seguimiento="TCK-2026-1002",
            id_cliente=cliente1.id_cliente if cliente1 else 1,
            titulo="Consulta sobre actualización de contraseña",
            descripcion="Quisiera saber cómo cambiar la contraseña de mi cuenta de correo de contacto.",
            categoria_preliminar="Acceso y Cuentas",
            prioridad="Baja",
            estado="Resuelto",
            respuesta_oficial="Estimada María, puede actualizar su clave desde la sección de Perfil de Usuario.",
            id_agente_asignado=agente1.id_agente if agente1 else 1
        )
        db.add(t2)
        db.commit()

    db.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    init_db()
