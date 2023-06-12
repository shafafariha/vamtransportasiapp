import streamlit as st
import numpy as np
import pandas as pd

def vam_solver(cost_matrix):
    # Fungsi untuk menyelesaikan persoalan transportasi menggunakan Metode VAM

    supply = cost_matrix[:, 0]
    demand = cost_matrix[0, :]
    num_supply = len(supply)
    num_demand = len(demand)
    allocation = np.zeros((num_supply, num_demand))
    supply_indices = np.arange(num_supply)
    demand_indices = np.arange(num_demand)

    while np.sum(supply) > 0 and np.sum(demand) > 0:
        penalties = []
        for i in supply_indices:
            for j in demand_indices:
                if allocation[i, j] == 0:
                    penalties.append((i, j, abs(supply[i] - demand[j])))

        penalties.sort(key=lambda x: x[2], reverse=True)

        min_supply_idx, min_demand_idx, _ = penalties[0]
        min_supply = min(supply[min_supply_idx], demand[min_demand_idx])

        allocation[min_supply_idx, min_demand_idx] = min_supply
        supply[min_supply_idx] -= min_supply
        demand[min_demand_idx] -= min_supply

    return allocation

def main():
    st.title("Persoalan Transportasi menggunakan VAM")

    num_supply = st.number_input("Jumlah Sumber Pasokan", min_value=1, step=1, value=1)
    num_demand = st.number_input("Jumlah Permintaan", min_value=1, step=1, value=1)

    cost_matrix = np.zeros((num_supply + 1, num_demand + 1))

    for i in range(num_supply):
        for j in range(num_demand):
            cost_matrix[i, j] = st.number_input(f"Biaya dari Sumber {i+1} ke Permintaan {j+1}",
                                                min_value=0, step=1, value=0)

    for i in range(num_supply):
        cost_matrix[i, num_demand] = st.number_input(f"Jumlah Pasokan dari Sumber {i+1}",
                                                        min_value=0, step=1, value=0)

    for j in range(num_demand):
        cost_matrix[num_supply, j] = st.number_input(f"Jumlah Permintaan ke Permintaan {j+1}",
                                                        min_value=0, step=1, value=0)

    if st.button("Selesaikan"):
        allocation = vam_solver(cost_matrix)

        supply = cost_matrix[:, 0]
        demand = cost_matrix[0, :]
        supply_indices = np.arange(num_supply)
        demand_indices = np.arange(num_demand)

        total_cost = np.sum(allocation * cost_matrix[:-1, :-1])

        st.header("Hasil Alokasi")
        allocation_df = pd.DataFrame(allocation,
                                    index=[f"Sumber {i+1}" for i in range(num_supply)],
                                    columns=[f"Permintaan {j+1}" for j in range(num_demand)])
        st.dataframe(allocation_df)

        st.header("Total Biaya")
        st.write(total_cost)

        st.header("Kelebihan Pasokan")
        supply_excess = pd.DataFrame(supply[:-1] - np.sum(allocation, axis=1),
                                    index=[f"Sumber {i+1}" for i in range(num_supply)],
                                    columns=["Kelebihan"])
        st.dataframe(supply_excess)

        st.header("Kekurangan Permintaan")
        demand_shortage = pd.DataFrame(demand[:-1] - np.sum(allocation, axis=0),
                                        index=[f"Permintaan {i+1}" for i in range(num_demand)],
                                        columns=["Kekurangan"])
        st.dataframe(demand_shortage)

if __name__ == '__main__':
    main()
