# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import date
from enum import Enum # Importar Enum desde el módulo enum

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="API de Gestión de Cobranzas para Pequeños Negocios",
    description="API para registrar deudas, gestionar clientes y enviar recordatorios."
)

# Configuración de CORS (Cross-Origin Resource Sharing)
# Esto es crucial para permitir que tu frontend (HTML/JS) se comunique con este backend
# En producción, deberías restringir 'allow_origins' a la URL de tu frontend.
origins = [
    "*",  # Permite todas las solicitudes de origen. ¡Cámbialo en producción!
    # "http://localhost:8000", # Ejemplo: Si tu frontend corre en localhost:8000
    # "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# --- Modelos de Datos (Pydantic) ---
# Define la estructura de los datos que se enviarán y recibirán.

# Modificación aquí: DebtStatus ahora hereda de str y Enum
class DebtStatus(str, Enum):
    """Enumeración para los estados de una deuda."""
    PENDING = "Pendiente"
    OVERDUE = "Atrasada"
    PAID = "Pagada"

class Debt(BaseModel):
    """Modelo para representar una deuda."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único de la deuda")
    client_name: str = Field(..., min_length=1, description="Nombre del cliente")
    amount: float = Field(..., gt=0, description="Monto de la deuda")
    due_date: date = Field(..., description="Fecha de vencimiento de la deuda (YYYY-MM-DD)")
    description: Optional[str] = Field(None, description="Descripción opcional de la deuda")
    status: DebtStatus = Field(DebtStatus.PENDING, description="Estado actual de la deuda")
    created_at: date = Field(default_factory=date.today, description="Fecha de creación de la deuda")

class DebtCreate(BaseModel):
    """Modelo para crear una nueva deuda (sin ID y estado por defecto)."""
    client_name: str = Field(..., min_length=1, description="Nombre del cliente")
    amount: float = Field(..., gt=0, description="Monto de la deuda")
    due_date: date = Field(..., description="Fecha de vencimiento de la deuda (YYYY-MM-DD)")
    description: Optional[str] = Field(None, description="Descripción opcional de la deuda")

class DebtUpdate(BaseModel):
    """Modelo para actualizar una deuda (todos los campos son opcionales)."""
    client_name: Optional[str] = Field(None, min_length=1, description="Nuevo nombre del cliente")
    amount: Optional[float] = Field(None, gt=0, description="Nuevo monto de la deuda")
    due_date: Optional[date] = Field(None, description="Nueva fecha de vencimiento")
    description: Optional[str] = Field(None, description="Nueva descripción de la deuda")
    status: Optional[DebtStatus] = Field(None, description="Nuevo estado de la deuda")

class Client(BaseModel):
    """Modelo para representar un cliente."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único del cliente")
    name: str = Field(..., min_length=1, description="Nombre del cliente")
    phone: str = Field(..., description="Número de teléfono del cliente (ej. +51987654321)")
    email: Optional[str] = Field(None, description="Correo electrónico del cliente")
    created_at: date = Field(default_factory=date.today, description="Fecha de registro del cliente")

class ClientCreate(BaseModel):
    """Modelo para crear un nuevo cliente."""
    name: str = Field(..., min_length=1, description="Nombre del cliente")
    phone: str = Field(..., description="Número de teléfono del cliente (ej. +51987654321)")
    email: Optional[str] = Field(None, description="Correo electrónico del cliente")

class ClientUpdate(BaseModel):
    """Modelo para actualizar un cliente."""
    name: Optional[str] = Field(None, min_length=1, description="Nuevo nombre del cliente")
    phone: Optional[str] = Field(None, description="Nuevo número de teléfono")
    email: Optional[str] = Field(None, description="Nuevo correo electrónico")


# --- Base de Datos en Memoria (para demostración) ---
# En una aplicación real, esto sería reemplazado por una base de datos persistente.
db_debts: List[Debt] = []
db_clients: List[Client] = []

# Datos de ejemplo para iniciar
db_clients.append(Client(id="client-1", name="Juan Pérez", phone="+51987654321", email="juan.perez@example.com"))
db_clients.append(Client(id="client-2", name="María García", phone="+51912345678", email="maria.garcia@example.com"))

db_debts.append(Debt(id="debt-1", client_name="Juan Pérez", amount=150.00, due_date=date(2025, 7, 15), status=DebtStatus.PENDING))
db_debts.append(Debt(id="debt-2", client_name="María García", amount=200.50, due_date=date(2025, 6, 30), status=DebtStatus.OVERDUE))
db_debts.append(Debt(id="debt-3", client_name="Carlos López", amount=75.00, due_date=date(2025, 7, 1), status=DebtStatus.PAID))


# --- Endpoints de Deudas ---

@app.post("/debts/", response_model=Debt, status_code=status.HTTP_201_CREATED, tags=["Deudas"])
async def create_debt(debt: DebtCreate):
    """
    Registra una nueva deuda en el sistema.
    """
    new_debt = Debt(
        client_name=debt.client_name,
        amount=debt.amount,
        due_date=debt.due_date,
        description=debt.description,
        status=DebtStatus.PENDING # Siempre se crea como pendiente
    )
    db_debts.append(new_debt)
    return new_debt

@app.get("/debts/", response_model=List[Debt], tags=["Deudas"])
async def get_all_debts(status: Optional[DebtStatus] = None):
    """
    Obtiene todas las deudas registradas, opcionalmente filtradas por estado.
    """
    if status:
        return [debt for debt in db_debts if debt.status == status]
    return db_debts

@app.get("/debts/{debt_id}", response_model=Debt, tags=["Deudas"])
async def get_debt(debt_id: str):
    """
    Obtiene una deuda específica por su ID.
    """
    for debt in db_debts:
        if debt.id == debt_id:
            return debt
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deuda no encontrada")

@app.put("/debts/{debt_id}", response_model=Debt, tags=["Deudas"])
async def update_debt(debt_id: str, debt_update: DebtUpdate):
    """
    Actualiza la información de una deuda existente.
    """
    for index, debt in enumerate(db_debts):
        if debt.id == debt_id:
            updated_data = debt_update.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(db_debts[index], key, value)
            return db_debts[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deuda no encontrada")

@app.delete("/debts/{debt_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Deudas"])
async def delete_debt(debt_id: str):
    """
    Elimina una deuda del sistema.
    """
    global db_debts
    initial_len = len(db_debts)
    db_debts = [debt for debt in db_debts if debt.id != debt_id]
    if len(db_debts) == initial_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deuda no encontrada")
    return {"message": "Deuda eliminada exitosamente"}

# --- Endpoints de Clientes ---

@app.post("/clients/", response_model=Client, status_code=status.HTTP_201_CREATED, tags=["Clientes"])
async def create_client(client: ClientCreate):
    """
    Registra un nuevo cliente en el sistema.
    """
    new_client = Client(
        name=client.name,
        phone=client.phone,
        email=client.email
    )
    db_clients.append(new_client)
    return new_client

@app.get("/clients/", response_model=List[Client], tags=["Clientes"])
async def get_all_clients():
    """
    Obtiene todos los clientes registrados.
    """
    return db_clients

@app.get("/clients/{client_id}", response_model=Client, tags=["Clientes"])
async def get_client(client_id: str):
    """
    Obtiene un cliente específico por su ID.
    """
    for client in db_clients:
        if client.id == client_id:
            return client
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@app.put("/clients/{client_id}", response_model=Client, tags=["Clientes"])
async def update_client(client_id: str, client_update: ClientUpdate):
    """
    Actualiza la información de un cliente existente.
    """
    for index, client in enumerate(db_clients):
        if client.id == client_id:
            updated_data = client_update.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(db_clients[index], key, value)
            return db_clients[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Clientes"])
async def delete_client(client_id: str):
    """
    Elimina un cliente del sistema.
    """
    global db_clients
    initial_len = len(db_clients)
    db_clients = [client for client in db_clients if client.id != client_id]
    if len(db_clients) == initial_len:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado exitosamente"}

# --- Endpoint de Recordatorios (Placeholder) ---

@app.post("/send-reminder/{debt_id}", tags=["Recordatorios"])
async def send_reminder(debt_id: str):
    """
    Envía un recordatorio de pago para una deuda específica.
    (Esta función es un placeholder y necesita integración real con Twilio/WhatsApp API)
    """
    debt = None
    for d in db_debts:
        if d.id == debt_id:
            debt = d
            break

    if not debt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deuda no encontrada")

    client = None
    for c in db_clients:
        if c.name == debt.client_name: # Asume que el nombre del cliente es único o busca por ID si lo implementas
            client = c
            break

    if not client or not client.phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Información de contacto del cliente no disponible.")

    # --- Lógica de Integración con Twilio/WhatsApp API ---
    # Aquí iría el código para usar la API de Twilio o WhatsApp.
    # Necesitarías:
    # 1. Tu Account SID y Auth Token de Twilio.
    # 2. Un número de teléfono de Twilio o un perfil de WhatsApp Business.
    # 3. Importar la librería de Twilio: `from twilio.rest import Client`
    #
    # Ejemplo conceptual (NO FUNCIONAL SIN CREDENCIALES Y LIBRERÍA):
    # from twilio.rest import Client
    # account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Tu Account SID
    # auth_token = "your_auth_token" # Tu Auth Token
    # twilio_client = Client(account_sid, auth_token)
    #
    # message_body = f"Hola {client.name}, te recordamos que tu deuda de ${debt.amount:.2f} vence el {debt.due_date}. ¡Gracias!"
    #
    # try:
    #     # Para SMS:
    #     message = twilio_client.messages.create(
    #         to=client.phone,
    #         from_="+15017122661", # Tu número de Twilio
    #         body=message_body
    #     )
    #     print(f"SMS enviado a {client.phone}: {message.sid}")
    #
    #     # Para WhatsApp (requiere configuración de WhatsApp Business API en Twilio):
    #     # message = twilio_client.messages.create(
    #     #     to=f"whatsapp:{client.phone}",
    #     #     from_="whatsapp:+14155238886", # Tu número de WhatsApp Twilio
    #     #     body=message_body
    #     # )
    #     # print(f"WhatsApp enviado a {client.phone}: {message.sid}")
    #
    # except Exception as e:
    #     print(f"Error al enviar recordatorio: {e}")
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al enviar recordatorio: {e}")

    # En este momento, solo simulamos el envío
    print(f"Simulando envío de recordatorio para la deuda {debt_id} al cliente {client.name} ({client.phone}).")
    return {"message": f"Recordatorio simulado enviado para la deuda {debt_id}"}

# Para ejecutar este servidor FastAPI, guarda el código como `main.py`
# y luego ejecuta en tu terminal: `uvicorn main:app --reload`
# La documentación interactiva (Swagger UI) estará disponible en http://127.0.0.1:8000/docs
