from threading import Lock

from app.models import Product, ProductRequest


class ProductStore:
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._next_id = 0
        self._lock = Lock()

        self.add(ProductRequest(name="Keyboard", description="Mechanical keyboard", price=89.90))
        self.add(ProductRequest(name="Monitor", description="27-inch 4K monitor", price=349.99))

    def get_all(self) -> list[Product]:
        with self._lock:
            return sorted(self._products.values(), key=lambda p: p.id)

    def get_by_id(self, product_id: int) -> Product | None:
        with self._lock:
            return self._products.get(product_id)

    def add(self, request: ProductRequest) -> Product:
        with self._lock:
            self._next_id += 1
            product = Product(id=self._next_id, **request.model_dump())
            self._products[product.id] = product
            return product

    def update(self, product_id: int, request: ProductRequest) -> Product | None:
        with self._lock:
            if product_id not in self._products:
                return None
            product = Product(id=product_id, **request.model_dump())
            self._products[product_id] = product
            return product

    def delete(self, product_id: int) -> bool:
        with self._lock:
            return self._products.pop(product_id, None) is not None
