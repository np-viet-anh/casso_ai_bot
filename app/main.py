from fastapi import FastAPI
from app.api.webhooks import router as webhook_router
from app.api.dashboard import router as dashboard_router
from app.db.database import Base, engine

# Tự động tạo bảng nếu chưa có (rất tiện cho Local test và Docker init)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Casso AI Bot")

# Đăng ký các rules (Routers)
app.include_router(webhook_router, tags=["Webhooks"])
app.include_router(dashboard_router, tags=["Dashboard"])

from fastapi.responses import RedirectResponse

@app.get("/")
def health_check():
    return RedirectResponse(url="/dashboard")
