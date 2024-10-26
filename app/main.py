from .config import app
from .routers.v1.customer_rentals import router as customer_rentals_router
from .routers.v1.customers import router as customers_router

app.include_router(router=customers_router, prefix="/api/v1")
app.include_router(router=customer_rentals_router, prefix="/api/v1")
