from src.ingest import generate_orders, generate_customers, generate_products


def test_orders_shape():
    df = generate_orders(100)
    assert len(df) == 100
    assert "order_id" in df.columns
    assert "line_total" not in df.columns  # computed in dbt


def test_customers_shape():
    df = generate_customers(50)
    assert len(df) == 50
    assert df["customer_id"].nunique() == 50


def test_products_shape():
    df = generate_products(20)
    assert len(df) == 20
    assert "category" in df.columns


def test_no_null_order_ids():
    df = generate_orders(1000)
    assert df["order_id"].notna().all()


def test_valid_status_values():
    df = generate_orders(1000)
    valid = {"completed", "pending", "cancelled", "refunded"}
    assert set(df["status"].unique()).issubset(valid)
