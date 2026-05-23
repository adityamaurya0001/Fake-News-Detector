import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os

class CafeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2c3e50")
        
        # Data storage
        self.menu_items = {
            "Coffee": {"Espresso": 120, "Cappuccino": 150, "Latte": 160, "Americano": 100},
            "Tea": {"Green Tea": 80, "Black Tea": 70, "Masala Chai": 60, "Iced Tea": 90},
            "Snacks": {"Sandwich": 150, "Burger": 200, "Pizza Slice": 180, "Fries": 100},
            "Desserts": {"Cake": 120, "Pastry": 90, "Ice Cream": 80, "Brownie": 110}
        }
        
        self.current_order = []
        self.order_history = []
        self.total_amount = 0
        
        # Load previous data
        self.load_data()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
    def create_header(self):
        header = tk.Frame(self.root, bg="#34495e", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="☕ CAFE MANAGEMENT SYSTEM", 
                        font=("Arial", 24, "bold"), bg="#34495e", fg="#ecf0f1")
        title.pack(pady=20)
        
    def create_main_content(self):
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel - Menu
        left_panel = tk.Frame(main_frame, bg="#34495e", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        menu_label = tk.Label(left_panel, text="MENU", font=("Arial", 16, "bold"), 
                             bg="#34495e", fg="#ecf0f1")
        menu_label.pack(pady=10)
        
        # Menu categories with notebook
        self.notebook = ttk.Notebook(left_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for category, items in self.menu_items.items():
            frame = tk.Frame(self.notebook, bg="#2c3e50")
            self.notebook.add(frame, text=category)
            
            for item, price in items.items():
                self.create_menu_item(frame, item, price, category)
        
        # Add/Edit Menu Button
        btn_frame = tk.Frame(left_panel, bg="#34495e")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Menu Item", command=self.add_menu_item,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 width=15, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Remove Item", command=self.remove_menu_item,
                 bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
                 width=15, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Middle Panel - Current Order
        middle_panel = tk.Frame(main_frame, bg="#34495e", width=350)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        order_label = tk.Label(middle_panel, text="CURRENT ORDER", 
                              font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1")
        order_label.pack(pady=10)
        
        # Order listbox
        list_frame = tk.Frame(middle_panel, bg="#34495e")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.order_listbox = tk.Listbox(list_frame, font=("Courier", 11),
                                        yscrollcommand=scrollbar.set,
                                        bg="#ecf0f1", selectmode=tk.SINGLE)
        self.order_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.order_listbox.yview)
        
        # Total and buttons
        self.total_label = tk.Label(middle_panel, text="Total: ₹0", 
                                   font=("Arial", 18, "bold"), bg="#34495e", fg="#f39c12")
        self.total_label.pack(pady=10)
        
        btn_frame2 = tk.Frame(middle_panel, bg="#34495e")
        btn_frame2.pack(pady=10)
        
        tk.Button(btn_frame2, text="Remove Selected", command=self.remove_from_order,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 width=15, cursor="hand2").pack(pady=5)
        
        tk.Button(btn_frame2, text="Clear Order", command=self.clear_order,
                 bg="#95a5a6", fg="white", font=("Arial", 10, "bold"),
                 width=15, cursor="hand2").pack(pady=5)
        
        tk.Button(btn_frame2, text="Process Payment", command=self.process_payment,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                 width=15, cursor="hand2", height=2).pack(pady=10)
        
        # Right Panel - Order History & Stats
        right_panel = tk.Frame(main_frame, bg="#34495e", width=300)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        history_label = tk.Label(right_panel, text="ORDER HISTORY", 
                                font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1")
        history_label.pack(pady=10)
        
        # History listbox
        hist_frame = tk.Frame(right_panel, bg="#34495e")
        hist_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        hist_scroll = tk.Scrollbar(hist_frame)
        hist_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(hist_frame, font=("Courier", 9),
                                         yscrollcommand=hist_scroll.set,
                                         bg="#ecf0f1")
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        hist_scroll.config(command=self.history_listbox.yview)
        
        # Statistics
        stats_frame = tk.Frame(right_panel, bg="#34495e")
        stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(stats_frame, text="Orders Today: 0\nRevenue: ₹0",
                                   font=("Arial", 12, "bold"), bg="#34495e", 
                                   fg="#ecf0f1", justify=tk.LEFT)
        self.stats_label.pack()
        
        tk.Button(stats_frame, text="Clear History", command=self.clear_history,
                 bg="#e67e22", fg="white", font=("Arial", 10, "bold"),
                 width=15, cursor="hand2").pack(pady=10)
        
    def create_footer(self):
        footer = tk.Frame(self.root, bg="#34495e", height=40)
        footer.pack(fill=tk.X)
        
        time_label = tk.Label(footer, text="", font=("Arial", 10), 
                            bg="#34495e", fg="#bdc3c7")
        time_label.pack(pady=10)
        
        def update_time():
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            time_label.config(text=current_time)
            self.root.after(1000, update_time)
        
        update_time()
        
    def create_menu_item(self, parent, item_name, price, category):
        item_frame = tk.Frame(parent, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        item_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(item_frame, text=item_name, font=("Arial", 11, "bold"),
                bg="#ecf0f1", anchor=tk.W).pack(side=tk.LEFT, padx=10)
        
        tk.Label(item_frame, text=f"₹{price}", font=("Arial", 11),
                bg="#ecf0f1", fg="#27ae60").pack(side=tk.RIGHT, padx=10)
        
        tk.Button(item_frame, text="Add", command=lambda: self.add_to_order(item_name, price),
                 bg="#3498db", fg="white", font=("Arial", 9, "bold"),
                 cursor="hand2").pack(side=tk.RIGHT, padx=5)
        
    def add_to_order(self, item, price):
        self.current_order.append({"item": item, "price": price})
        self.order_listbox.insert(tk.END, f"{item:<25} ₹{price}")
        self.total_amount += price
        self.total_label.config(text=f"Total: ₹{self.total_amount}")
        
    def remove_from_order(self):
        selection = self.order_listbox.curselection()
        if selection:
            idx = selection[0]
            self.total_amount -= self.current_order[idx]["price"]
            self.total_label.config(text=f"Total: ₹{self.total_amount}")
            del self.current_order[idx]
            self.order_listbox.delete(idx)
        else:
            messagebox.showwarning("Warning", "Please select an item to remove")
            
    def clear_order(self):
        if messagebox.askyesno("Confirm", "Clear entire order?"):
            self.current_order = []
            self.order_listbox.delete(0, tk.END)
            self.total_amount = 0
            self.total_label.config(text="Total: ₹0")
            
    def process_payment(self):
        if not self.current_order:
            messagebox.showwarning("Warning", "No items in order")
            return
            
        payment = simpledialog.askfloat("Payment", 
                                        f"Total Amount: ₹{self.total_amount}\nEnter payment amount:")
        
        if payment is None:
            return
            
        if payment >= self.total_amount:
            change = payment - self.total_amount
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            order_record = {
                "timestamp": timestamp,
                "items": self.current_order.copy(),
                "total": self.total_amount,
                "payment": payment,
                "change": change
            }
            
            self.order_history.append(order_record)
            self.history_listbox.insert(0, f"{timestamp} - ₹{self.total_amount}")
            
            messagebox.showinfo("Success", 
                              f"Payment Successful!\nChange: ₹{change:.2f}\n\nThank you!")
            
            self.clear_order()
            self.update_stats()
            self.save_data()
        else:
            messagebox.showerror("Error", "Insufficient payment amount")
            
    def add_menu_item(self):
        category = simpledialog.askstring("Category", "Enter category name:")
        if not category:
            return
            
        item_name = simpledialog.askstring("Item", "Enter item name:")
        if not item_name:
            return
            
        price = simpledialog.askfloat("Price", "Enter price:")
        if price is None:
            return
            
        if category not in self.menu_items:
            self.menu_items[category] = {}
            
        self.menu_items[category][item_name] = price
        messagebox.showinfo("Success", f"Added {item_name} to {category}")
        self.refresh_menu()
        self.save_data()
        
    def remove_menu_item(self):
        category = simpledialog.askstring("Category", "Enter category name:")
        if not category or category not in self.menu_items:
            messagebox.showerror("Error", "Category not found")
            return
            
        item_name = simpledialog.askstring("Item", "Enter item name to remove:")
        if not item_name or item_name not in self.menu_items[category]:
            messagebox.showerror("Error", "Item not found")
            return
            
        del self.menu_items[category][item_name]
        messagebox.showinfo("Success", f"Removed {item_name}")
        self.refresh_menu()
        self.save_data()
        
    def refresh_menu(self):
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
            
        for category, items in self.menu_items.items():
            frame = tk.Frame(self.notebook, bg="#2c3e50")
            self.notebook.add(frame, text=category)
            
            for item, price in items.items():
                self.create_menu_item(frame, item, price, category)
                
    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all order history?"):
            self.order_history = []
            self.history_listbox.delete(0, tk.END)
            self.update_stats()
            self.save_data()
            
    def update_stats(self):
        today_orders = len(self.order_history)
        total_revenue = sum(order["total"] for order in self.order_history)
        self.stats_label.config(text=f"Orders Today: {today_orders}\nRevenue: ₹{total_revenue}")
        
    def save_data(self):
        data = {
            "menu": self.menu_items,
            "history": self.order_history
        }
        with open("cafe_data.json", "w") as f:
            json.dump(data, f, indent=4)
            
    def load_data(self):
        if os.path.exists("cafe_data.json"):
            try:
                with open("cafe_data.json", "r") as f:
                    data = json.load(f)
                    self.menu_items = data.get("menu", self.menu_items)
                    self.order_history = data.get("history", [])
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeManagementSystem(root)
    root.mainloop()