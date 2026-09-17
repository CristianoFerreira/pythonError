from fastapi import FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.models import Product, ProductRequest
from app.store import ProductStore

app = FastAPI(
    title="Product API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/swagger",
)

store = ProductStore()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": exc.errors()[0]["msg"]})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[Product])
def get_products() -> list[Product]:
    return store.get_all()


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    product = store.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=Product, status_code=201)
def create_product(request: ProductRequest, response: Response) -> Product:
    created = store.add(request)
    response.headers["Location"] = f"/products/{created.id}"
    return created


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, request: ProductRequest) -> Product:
    updated = store.update(product_id, request)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int) -> Response:
    if not store.delete(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return Response(status_code=204)
