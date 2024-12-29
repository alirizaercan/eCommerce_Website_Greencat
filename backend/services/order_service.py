# backend/services/order_service.py
from models.order_details import OrderDetails
from models.order_items import OrderItems
from models.product import Product
from models.customer import Customer
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

class OrderService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_order(self, customer_id: int, total: float, tax: float, order_status: str, payment_id: int):
        order = OrderDetails(customer_id=customer_id, total=total, tax=tax, order_status=order_status, payment_id=payment_id)
        self.db_session.add(order)
        self.db_session.commit()
        return order

    def get_all_orders(self):
        return (self.db_session.query(OrderDetails)
                .options(joinedload(OrderDetails.items)
                        .joinedload(OrderItems.product))
                .order_by(OrderDetails.created_at.desc())
                .all())

    def get_customer_orders(self, customer_id: int):
        try:
            orders = self.db_session.query(OrderDetails)\
                .filter(OrderDetails.customer_id == customer_id)\
                .options(
                    joinedload(OrderDetails.items)
                    .joinedload(OrderItems.product)
                    .joinedload(Product.images)
                )\
                .order_by(OrderDetails.created_at.desc())\
                .all()
            
            return [self._format_order(order) for order in orders]
        except Exception as e:
            print(f"Error fetching orders: {str(e)}")
            raise

    def _format_order(self, order):
        return {
            'order_id': order.order_id,
            'customer_id': order.customer_id,
            'total': float(order.total),
            'tax': float(order.tax),
            'order_status': order.order_status,
            'created_at': order.created_at.isoformat(),
            'items': [self._format_order_item(item) for item in order.items]
        }

    def _format_order_item(self, item):
        product = item.product
        try:
            image_url = None
            if product and hasattr(product, 'images') and product.images:
                image_url = product.images[0].image_url
                
            return {
                'item_id': item.order_item_id,
                'quantity': item.quantity,
                'product': {
                    'product_id': product.product_id,
                    'name': product.product_name,
                    'price': float(product.price),
                    'description': product.description,
                    'image_url': image_url,
                    'category_name': product.category.category_name if product.category else None,
                    'discount': {
                        'discount_percentage': product.discount.discount_percentage
                    } if product.discount else None
                }
            }
        except Exception as e:
            print(f"Error formatting order item: {str(e)}")
            return None

    def format_orders(self, orders):
        formatted_orders = []
        for order in orders:
            items = []
            for item in order.items:
                product = item.product
                if not product:
                    continue
                    
                # Get the first image URL or default to None
                image_url = product.images[0].image_url if product.images else None
                    
                items.append({
                    'item_id': item.order_item_id,
                    'quantity': item.quantity,
                    'product': {
                        'product_id': product.product_id,
                        'name': product.product_name,
                        'price': float(product.price),
                        'description': product.description,
                        'image_url': image_url,
                        'category_name': product.category.category_name if product.category else None,
                        'discount': {
                            'discount_percentage': product.discount.discount_percentage
                        } if product.discount else None
                    }
                })

            order_dict = {
                'order_id': order.order_id,
                'customer_id': order.customer_id,
                'total': float(order.total),
                'tax': float(order.tax),
                'order_status': order.order_status,
                'created_at': order.created_at.isoformat(),
                'items': items
            }
            formatted_orders.append(order_dict)
        
        return formatted_orders

    def get_order_items(self, order_id: int):
        """Get all order items with complete product details"""
        items = (self.db_session.query(OrderItems)
                .filter(OrderItems.order_id == order_id)
                .join(OrderItems.product)
                .options(
                    joinedload(OrderItems.product).joinedload(Product.images),
                    joinedload(OrderItems.product).joinedload(Product.category),
                    joinedload(OrderItems.product).joinedload(Product.discount)
                )
                .all())
        
        result = []
        for item in items:
            product = item.product
            item_dict = {
                'item_id': item.order_item_id,
                'quantity': item.quantity,
                'product': {
                    'product_id': product.product_id,
                    'name': product.product_name,
                    'price': float(product.price),
                    'description': product.description,
                    'image_url': product.images[0].image_url if product.images else None,
                    'category_name': product.category.category_name if product.category else None,
                    'discount': {
                        'discount_percentage': product.discount.discount_percentage
                    } if product.discount else None
                }
            }
            result.append(item_dict)
        
        return result

    def format_orders(self, orders):
        formatted_orders = []
        for order in orders:
            order_dict = {
                'order_id': order.order_id,
                'customer_id': order.customer_id,
                'total': float(order.total),
                'tax': float(order.tax),
                'order_status': order.order_status,
                'created_at': order.created_at.isoformat(),
                'items': self.get_order_items(order.order_id)
            }
            formatted_orders.append(order_dict)
        
        return formatted_orders
        
    def get_order_details(self, order_id: int):
        return (self.db_session.query(OrderDetails)
                .filter(OrderDetails.order_id == order_id)
                .options(
                    joinedload(OrderDetails.items)
                    .joinedload(OrderItems.product)
                )
                .first())

    def get_order_by_id(self, order_id: int):
        return (self.db_session.query(OrderDetails)
                .filter(OrderDetails.order_id == order_id)
                .options(
                    joinedload(OrderDetails.items)
                    .joinedload(OrderItems.product)
                )
                .first())

    def update_order(self, order_id: int, total: float, tax: float, order_status: str, payment_id: int):
        order = self.db_session.query(OrderDetails).filter(OrderDetails.order_id == order_id).first()
        if order:
            order.total = total
            order.tax = tax
            order.order_status = order_status
            order.payment_id = payment_id
            self.db_session.commit()
        return order

    def delete_order(self, order_id: int):
        order = self.db_session.query(OrderDetails).filter(OrderDetails.order_id == order_id).first()
        if order:
            self.db_session.delete(order)
            self.db_session.commit()
        return order

    def add_order_item(self, order_id: int, product_id: int, quantity: int):
        order_item = OrderItems(order_id=order_id, product_id=product_id, quantity=quantity)
        self.db_session.add(order_item)
        self.db_session.commit()
        return order_item
    
    def create_order_with_items(self, customer_id: int, total: float, tax: float, order_status: str, payment_id: int, items: list):
        # Create the order
        order = OrderDetails(customer_id=customer_id, total=total, tax=tax, order_status=order_status, payment_id=payment_id)
        self.db_session.add(order)
        
        # Commit the order first to generate order_id
        self.db_session.commit()
        self.db_session.refresh(order)

        # Add order items
        for item in items:
            order_item = OrderItems(
                order_id=order.order_id,
                product_id=item['product_id'],
                quantity=item['quantity']
            )
            self.db_session.add(order_item)
        
        # Commit the transaction for items
        self.db_session.commit()
        
        # Return the order with the items
        return order

    def update_order_item(self, order_item_id: int, quantity: int):
        order_item = self.db_session.query(OrderItems).filter(OrderItems.order_item_id == order_item_id).first()
        if order_item:
            order_item.quantity = quantity
            self.db_session.commit()
        return order_item

    def delete_order_item(self, order_item_id: int):
        order_item = self.db_session.query(OrderItems).filter(OrderItems.order_item_id == order_item_id).first()
        if order_item:
            self.db_session.delete(order_item)
            self.db_session.commit()
        return order_item
        
    def get_order_summary(self, order_id: int):
        order = self.db_session.query(OrderDetails).filter(OrderDetails.order_id == order_id).first()
        if not order:
            return None

        # Siparişin item'larını alıyoruz
        items = self.db_session.query(OrderItems).filter(OrderItems.order_id == order_id).all()

        summary = {
            'items': [{
                'product_id': item.product_id,
                'quantity': item.quantity,
                'subtotal': item.product.price * item.quantity,  # Burada price bilgisini almanız gerekebilir
                'tax_amount': item.product.price * item.quantity * 0.18  # Örnek, vergi oranı %18
            } for item in items],
            'total_items': sum(item.quantity for item in items),
            'subtotal': sum(item.product.price * item.quantity for item in items),
            'total_tax': sum(item.product.price * item.quantity * 0.18 for item in items),  # Örnek, vergi oranı %18
            'total': order.total
        }
        return summary
