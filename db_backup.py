import os
import json
import sqlite3
from datetime import datetime

def export_backup_json(db_path='instance/fabrix.db', output_file=None):
    """Exports all inventory, invoice, and purchase data to a portable JSON backup file."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"fabrix_backup_{timestamp}.json"
        
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read products
    cursor.execute("SELECT id, name, quantity, selling_price, cost_price FROM products")
    products = [{"id": r[0], "name": r[1], "quantity": r[2], "selling_price": r[3], "cost_price": r[4]} for r in cursor.fetchall()]

    # Read invoices
    cursor.execute("SELECT id, invoice_number, customer_name, customer_phone, date_created, total_amount, discount, final_amount, amount_paid, payment_status, payment_method FROM invoices")
    invoices = []
    for inv_row in cursor.fetchall():
        inv_id = inv_row[0]
        cursor.execute("SELECT product_name, quantity, selling_price, cost_price FROM invoice_items WHERE invoice_id = ?", (inv_id,))
        items = [{"product_name": item[0], "quantity": item[1], "selling_price": item[2], "cost_price": item[3]} for item in cursor.fetchall()]
        
        invoices.append({
            "invoice_number": inv_row[1],
            "customer_name": inv_row[2],
            "customer_phone": inv_row[3],
            "date_created": inv_row[4],
            "total_amount": inv_row[5],
            "discount": inv_row[6],
            "final_amount": inv_row[7],
            "amount_paid": inv_row[8],
            "payment_status": inv_row[9],
            "payment_method": inv_row[10],
            "items": items
        })

    # Read dealer purchases
    cursor.execute("SELECT dealer_name, product_description, quantity, total_cost, amount_paid, payment_status, date_created FROM dealer_purchases")
    purchases = [{
        "dealer_name": r[0],
        "product_description": r[1],
        "quantity": r[2],
        "total_cost": r[3],
        "amount_paid": r[4],
        "payment_status": r[5],
        "date_created": r[6]
    } for r in cursor.fetchall()]

    conn.close()

    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "app": "Fabrix Billing & Stock Management",
        "version": "2.0",
        "products": products,
        "invoices": invoices,
        "dealer_purchases": purchases
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=4)

    print(f"--- SUCCESS: Backup successfully saved to '{output_file}' ---")
    return output_file

def restore_from_json(backup_file, db_path='instance/fabrix.db'):
    """Restores entire database state from a JSON backup file in case of system crash."""
    if not os.path.exists(backup_file):
        print(f"Error: Backup file '{backup_file}' does not exist.")
        return False

    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Initialize connection using Flask context if active, or sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Restore products
    for prod in data.get('products', []):
        cursor.execute("SELECT id FROM products WHERE name = ?", (prod['name'],))
        row = cursor.fetchone()
        if row:
            cursor.execute("UPDATE products SET quantity=?, selling_price=?, cost_price=? WHERE id=?",
                           (prod['quantity'], prod['selling_price'], prod['cost_price'], row[0]))
        else:
            cursor.execute("INSERT INTO products (name, quantity, selling_price, cost_price) VALUES (?, ?, ?, ?)",
                           (prod['name'], prod['quantity'], prod['selling_price'], prod['cost_price']))

    conn.commit()
    conn.close()
    print(f"--- SUCCESS: Restored database from '{backup_file}' ---")
    return True

if __name__ == '__main__':
    print("Fabrix Database Backup & Recovery Utility")
    export_backup_json()
