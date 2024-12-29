from flask import Blueprint, request, jsonify, current_app
from services.admin_service import AdminService
from utils.database import Database
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
admin_controller = Blueprint('admin_controller', __name__)
db = Database()

def validate_graph_request(data):
    valid_graph_types = [
        "Gelir Analizi", "Ürün Satışları", 
        "Müşteri Aktivitesi", "Sipariş Durumu",
        "Kategori Performansı"
    ]
    if data['graph_type'] not in valid_graph_types:
        raise ValueError(f"Invalid graph type. Must be one of: {', '.join(valid_graph_types)}")
    
    try:
        datetime.strptime(data['start_date'], '%Y-%m-%d')
        datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def _generate_plot(graph_type, graph_data):
    """Helper function to generate different types of plots"""
    try:
        if graph_type == "Gelir Analizi":
            providers = [data['provider'] for data in graph_data]
            revenue = [float(data['total_revenue']) for data in graph_data]
            transactions = [data['transaction_count'] for data in graph_data]

            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()

            x = range(len(providers))
            ax1.bar(x, revenue, color='b', alpha=0.7, label='Revenue')
            ax2.plot(x, transactions, 'r-o', label='Transactions')

            plt.xticks(x, providers, rotation=45)
            ax1.set_xlabel('Ödeme Sağlayıcısı')
            ax1.set_ylabel('Gelir (TL)', color='b')
            ax2.set_ylabel('İşlem Sayısı', color='r')
            plt.title('Ödeme Sağlayıcılarına Göre Gelir Analizi')
            
        elif graph_type == "Ürün Satışları":
            products = [data['product_name'] for data in graph_data]
            units = [data['units_sold'] for data in graph_data]
            revenue = [float(data['revenue']) for data in graph_data]
            
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()
            
            x = np.arange(len(products))
            width = 0.35
            
            bars = ax1.bar(x, revenue, width, color='g', alpha=0.7, label='Revenue')
            lines = ax2.plot(x, units, 'r-o', label='Units Sold')
            
            total_revenue = sum(revenue)
            total_units = sum(units)
            
            plt.title(f'En Çok Satan 10 Ürün\nToplam Gelir: {total_revenue:,.2f} TL | Toplam Satış: {total_units:,} Adet')
            ax1.set_xlabel('Ürünler')
            ax1.set_ylabel('Gelir (TL)', color='g')
            ax2.set_ylabel('Satış Adedi', color='r')
            
            ax1.set_xticks(x)
            ax1.set_xticklabels(products, rotation=45, ha='right')
            
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
            
            plt.tight_layout()

        elif graph_type == "Müşteri Aktivitesi":
            cities = [data['city'] for data in graph_data]
            sessions = [data['session_count'] for data in graph_data]
            avg_value = [float(data['avg_cart_value']) for data in graph_data]

            fig, ax1 = plt.subplots(figsize=(12, 8))  # Increased height
            ax2 = ax1.twinx()

            ax1.bar(cities, sessions, color='b', alpha=0.7, label='Sessions')
            ax2.plot(cities, avg_value, 'r-o', label='Avg Cart Value')

            plt.title('Şehirlere Göre Müşteri Aktivitesi')
            ax1.set_xlabel('Şehirler')
            ax1.set_ylabel('Oturum Sayısı', color='b')
            ax2.set_ylabel('Ortalama Sepet Tutarı (TL)', color='r')
            
            # Vertical labels with alignment
            plt.xticks(rotation=90, ha='center')
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()

        elif graph_type == "Sipariş Durumu":
            statuses = [data['order_status'] for data in graph_data]
            counts = [data['order_count'] for data in graph_data]
            values = [float(data['total_value']) for data in graph_data]

            plt.figure(figsize=(12, 6))
            plt.pie(values, labels=statuses, autopct='%1.1f%%')
            plt.title('Sipariş Durumu Dağılımı')

        elif graph_type == "Kategori Performansı":
            categories = [data['category_name'] for data in graph_data]
            products = [data['product_count'] for data in graph_data]
            discounts = [float(data['avg_discount']) for data in graph_data]
            sold = [data['total_sold'] for data in graph_data]

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

            ax1.bar(categories, products, color='b', alpha=0.7)
            ax1.set_title('Kategorilere Göre Ürün Sayısı')
            ax1.set_xlabel('Kategoriler')
            ax1.set_ylabel('Ürün Sayısı')

            ax2.bar(categories, sold, color='g', alpha=0.7)
            ax2_twin = ax2.twinx()
            ax2_twin.plot(categories, discounts, 'r-o')
            ax2.set_xlabel('Kategoriler')
            ax2.set_ylabel('Satış Adedi', color='g')
            ax2_twin.set_ylabel('Ortalama İndirim %', color='r')

            plt.xticks(rotation=45)

        plt.tight_layout()

    except Exception as e:
        logger.error(f"Grafik oluşturma hatası: {str(e)}")
        raise ValueError(f"{graph_type} grafiği oluşturulamadı")

@admin_controller.route('/login', methods=['POST'])
def admin_login():
    """Admin login endpoint with enhanced error handling"""
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid content type'}), 415
        
    try:
        data = request.json
        if not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Missing credentials'}), 400

        engine = db.engine
        admin_service = AdminService(engine)
        
        admin_user = admin_service.authenticate_admin(data['username'], data['password'])
        
        if not admin_user:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
        return jsonify({
            'success': True,
            'admin': {
                'username': admin_user.username,
                'type': admin_user.admin_type.admin_type_name,
                'permissions': admin_user.admin_type.permissions
            }
        })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_controller.route('/graphs/data', methods=['POST'])
def get_graph_data():
    """Get graph data with enhanced validation"""
    if not request.is_json:
        return jsonify({'error': 'Invalid content type'}), 415
        
    session = None
    try:
        data = request.json
        validate_graph_request(data)
        
        # Use get_session() instead of connect()
        session = db.get_session()
        service = AdminService(db.engine)
        graph_data = service.get_graph_data(
            data['graph_type'],
            data['start_date'],
            data['end_date']
        )
        
        if not graph_data:
            return jsonify({'message': 'No data found'}), 404
            
        return jsonify(graph_data), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Graph data error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if session:
            db.close(session)

@admin_controller.route('/graphs/generate', methods=['POST'])
def generate_graph():
    """Generate graph with improved error handling and cleanup"""
    if not request.is_json:
        return jsonify({'error': 'Invalid content type'}), 415
        
    session = None
    try:
        data = request.json
        validate_graph_request(data)
        
        session = db.get_session()
        service = AdminService(db.engine)
        graph_data = service.get_graph_data(
            data['graph_type'],
            data['start_date'],
            data['end_date']
        )

        if not graph_data:
            return jsonify({'error': 'No data available'}), 404

        # Set matplotlib style before creating figure
        plt.style.use('default')  # Use default style instead of seaborn
        sns.set_theme()  # Apply seaborn theme after setting style
        
        plt.figure(figsize=(12, 6))
        
        _generate_plot(data['graph_type'], graph_data)

        static_dir = os.path.join(current_app.root_path, 'static', 'graphs', 'admin_graphs')
        os.makedirs(static_dir, exist_ok=True)
        
        file_name = f"{data['graph_type'].replace(' ', '_')}_{data['start_date']}_{data['end_date']}.png"
        file_path = os.path.join(static_dir, file_name)
        
        plt.savefig(file_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        return jsonify({
            'message': 'Graph generated successfully',
            'path': f'/static/graphs/admin_graphs/{file_name}'
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Graph generation error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if session:
            db.close(session)
        plt.close('all')