
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cosmetic Product LCA Calculator", layout="wide")

st.title("Cosmetic Product LCA Calculator")

st.markdown("""
This tool estimates the carbon emissions (CO₂-eq) from the life cycle of a cosmetic product.
You can input multiple ingredients, packaging details, and usage patterns.
""")

# Step 1: Basic Product Info
st.header("Product Information")
product_name = st.text_input("Product Name", "Moisturizing Cream")
product_weight_grams = st.number_input("Product Weight (g)", min_value=10, max_value=1000, value=100)

# Step 2: Ingredients Table
st.header("Ingredients")
ingredient_df = st.data_editor(
    pd.DataFrame(columns=["Ingredient Name", "Percentage", "Emission Factor (g CO₂-eq/kg)"]),
    num_rows="dynamic",
    key="ingredients_editor"
)

# Step 3: Packaging and Manufacturing
st.header("Packaging and Manufacturing")
packaging_weight = st.number_input("Packaging Weight (g)", value=50)
packaging_emission_factor = st.number_input("Packaging Emission Factor (g CO₂-eq/g)", value=2.0)
energy_used = st.number_input("Manufacturing Energy (kWh/unit)", value=0.5)
energy_emission_factor = st.number_input("Electricity Emission Factor (g CO₂-eq/kWh)", value=400)

# Step 4: Transport and Use
st.header("Transport and Use Phase")
distance_km = st.number_input("Transport Distance (km)", value=500)
transport_emission_factor = st.number_input("Transport Emission Factor (g CO₂-eq/tkm)", value=62)
water_use = st.number_input("Hot Water Use per Application (L)", value=2.0)
water_emission_factor = st.number_input("Water Heating Emission Factor (g CO₂-eq/L)", value=0.3)

# Step 5: End of Life
st.header("End-of-Life")
disposal_emissions = st.number_input("Disposal Emissions per Unit (g CO₂-eq)", value=10)

# Calculation
if st.button("Calculate Emissions"):
    st.subheader("Emission Breakdown")

    product_weight_kg = product_weight_grams / 1000

    # Convert table values to numeric
    ingredient_df["Percentage"] = pd.to_numeric(ingredient_df["Percentage"], errors="coerce").fillna(0)
    ingredient_df["Emission Factor (g CO₂-eq/kg)"] = pd.to_numeric(
        ingredient_df["Emission Factor (g CO₂-eq/kg)"], errors="coerce"
    ).fillna(0)

    # Calculate emissions
    ingredient_emissions = (
        (ingredient_df["Percentage"] / 100) * product_weight_kg * ingredient_df["Emission Factor (g CO₂-eq/kg)"]
    ).sum()

    packaging_emissions = packaging_weight * packaging_emission_factor
    manufacturing_emissions = energy_used * energy_emission_factor
    transport_emissions = (product_weight_kg / 1000) * distance_km * transport_emission_factor
    use_phase_emissions = water_use * water_emission_factor
    total_emissions = sum([
        ingredient_emissions, packaging_emissions, manufacturing_emissions,
        transport_emissions, use_phase_emissions, disposal_emissions
    ])

    st.metric("Total Emissions", f"{total_emissions:.2f} g CO₂-eq")

    st.write("**Breakdown:**")
    st.json({
        "Ingredients": f"{ingredient_emissions:.2f} g",
        "Packaging": f"{packaging_emissions:.2f} g",
        "Manufacturing": f"{manufacturing_emissions:.2f} g",
        "Transport": f"{transport_emissions:.2f} g",
        "Use Phase": f"{use_phase_emissions:.2f} g",
        "Disposal": f"{disposal_emissions:.2f} g"
    })
