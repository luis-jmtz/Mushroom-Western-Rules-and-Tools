import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
from abilities import *
import streamlit as st

# Load data to get accurate names lists 
abilities_df = pd.read_csv(r"Data\Creature_abilities.tsv", sep="\t")
creature_types = pd.read_csv(r"Data\creature_types.tsv", sep="\t")
armor_df = pd.read_csv(r"Data\Armor.tsv", sep="\t")
shields_df = pd.read_csv(r"Data\Shields.tsv", sep="\t")
melee_df = pd.read_csv(r"Data\Melee.tsv", sep="\t")
projectile_df = pd.read_csv(r"Data\Projectile.tsv", sep="\t")
firearms_df = pd.read_csv(r"Data\Firearms.tsv", sep="\t")
explosives_df = pd.read_csv(r"Data\Explosives.tsv", sep="\t")
weapons_df_list = [melee_df, projectile_df, firearms_df]

# ------------------------------ Helper functions for dropdowns ----------------------------- # 

def get_armor_options():
    return {f"{row['name']} (AC: {row['AC']})": row['id'] for _, row in armor_df.iterrows()}

def get_shield_options():
    return {f"{row['name']} (AC: {row['ac']})": row['id'] for _, row in shields_df.iterrows()}

def get_weapon_options(weapon_type):
    weapon_names = {
        0: "Melee",
        1: "Projectile", 
        2: "Firearms"
    }
    df = weapons_df_list[weapon_type]
    return {f"{row['name']} (Dmg: {row['dmg']})": row['id'] for _, row in df.iterrows()}

def get_explosive_options():
    return {f"{row['name']} (Dmg: {row['dmg']}, Radius: {row['radius']})": row['id'] for _, row in explosives_df.iterrows()}

def get_ability_options():
    return {f"{row['name']} (Type: {row['type']}, Points: {row['points']})": row['id'] for _, row in abilities_df.iterrows()}




# ----------------------------------------  Streamlit App Start ------------------------- #
st.title("Creature Creator")

st.header("Create New Creature")

with st.form("creature_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        creature_name = st.text_input("Creature Name", "Unnamed Creature")


        chosen_creature_type = st.selectbox(
            "Creature Type",
            creature_types["name"]
        )

        level = st.number_input("Level", 0, 20, 1)
        size = st.selectbox("Size", 
                           ["Small (-1)", "Medium (0)", "Large (1)", "Huge (2)"],
                           index=1)
        size_map = {"Small (-1)": -1, "Medium (0)": 0, "Large (1)": 1, "Huge (2)": 2}
        size_value = size_map[size]
        
        st.subheader("Movement")
        base_speed = st.number_input("Base Speed", 0, 20, 6)
        can_fly = st.checkbox("Can Fly")
        can_burrow = st.checkbox("Can Burrow")
        
        st.subheader("Action Economy")
        ap = st.number_input("AP", 2, 10, 2)
        num_attacks = st.number_input("Number of Attacks", 1, 5, 1)
        focus_points = st.number_input("FP", 0, 10, 0)
    

    # ----------------------- Attributes ------------------ #

    with col2:
        st.subheader("Attributes")
        brawn = st.number_input("Brawn", -5, 10, 0)
        reflex = st.number_input("Reflex", -5, 10, 0)
        brains = st.number_input("Brains", -5, 10, 0)
        mettle = st.number_input("Mettle", -5, 10, 0)
        

        # ----------------------- Equipment ------------------ #
        st.subheader("Equipment")
        armor_options = get_armor_options()
        selected_armor = st.selectbox("Armor", ["None"] + list(armor_options.keys()))
        
        shield_options = get_shield_options()
        selected_shield = st.selectbox("Shield", ["None"] + list(shield_options.keys()))
        
    # Weapons section
    st.subheader("Weapons")
    
    weapons_to_add = []
    
    st.write("Melee Weapons")
    melee_options = get_weapon_options(0)
    selected_melee = st.multiselect("Select Melee Weapons", list(melee_options.keys()))
    weapons_to_add.extend([(0, melee_options[w]) for w in selected_melee])
    
    st.write("Projectile Weapons")
    projectile_options = get_weapon_options(1)
    selected_projectile = st.multiselect("Select Projectile Weapons", list(projectile_options.keys()))
    weapons_to_add.extend([(1, projectile_options[w]) for w in selected_projectile])
    
    st.write("Firearms")
    firearm_options = get_weapon_options(2)
    selected_firearms = st.multiselect("Select Firearms", list(firearm_options.keys()))
    weapons_to_add.extend([(2, firearm_options[w]) for w in selected_firearms])
    
    # Explosives section
    st.subheader("Explosives")
    
    explosive_options = get_explosive_options()
    selected_explosives = st.multiselect("Select Explosives", list(explosive_options.keys()))
    
    explosive_counts = {}
    for explosive in selected_explosives:
        count = st.number_input(f"Count for {explosive}", 1, 100, 1, key=f"exp_{explosive}")
        explosive_counts[explosive_options[explosive]] = count
    
    # Abilities section
    st.subheader("Abilities")
    ability_options = get_ability_options()
    selected_abilities = st.multiselect("Select Abilities", list(ability_options.keys()))
    
    # Submit button
    submitted = st.form_submit_button("Create Creature")
    
    if submitted:
        # Create the creature
        creature = Creature()
        creature.level = level
        creature.size = size_value
        creature.base_speed = base_speed
        creature.canFly = can_fly
        creature.canBurrow = can_burrow
        creature.ap = ap
        creature.num_attacks = num_attacks
        creature.focus_points = focus_points
        
        # Set attributes
        creature.brawn = brawn
        creature.reflex = reflex
        creature.brains = brains
        creature.mettle = mettle
        
        # Add equipment
        if selected_armor != "None":
            creature.add_armor(armor_options[selected_armor])
        
        if selected_shield != "None":
            creature.add_shield(shield_options[selected_shield])
        
        # Add weapons
        for weapon_type, weapon_id in weapons_to_add:
            creature.add_weapon(weapon_type, weapon_id)
        
        # Add explosives
        for explosive_id, count in explosive_counts.items():
            creature.add_explosives(explosive_id, count)
        
        # Add abilities
        for ability in selected_abilities:
            creature.add_ability(ability_options[ability])
        
        # Calculate stats
        creature.calc_bonuses()
        creature.calc_ac()
        creature.calc_dpr()
        difficulty = creature.calculate_difficulty()
        
        # Generate formatted markdown output
        markdown_output = f"## {creature_name}\n\n"
        
        # Basic Info - only show non-default values
        basic_info = []
        basic_info.append(f"**Level**: {creature.level}")
        if size != "Medium (0)":
            basic_info.append(f"**Size**: {size}")
        if creature.speed != 6:
            basic_info.append(f"**Speed**: {creature.speed}")
        if creature.canFly:
            basic_info.append("**Flight**: Yes")
        if creature.canBurrow:
            basic_info.append("**Burrow**: Yes")
        
        if basic_info:
            markdown_output +=  "  \n".join(basic_info) + f", {chosen_creature_type}\n\n"
        
        # Attributes Table
        markdown_output += "### Attributes\n"
        markdown_output += "| Brawn | Reflex | Brains | Mettle |\n"
        markdown_output += "|-------|--------|--------|--------|\n"
        markdown_output += f"| {creature.brawn} | {creature.reflex} | {creature.brains} | {creature.mettle} |\n\n"
        
        # Combat Stats - only show non-zero/non-default values
        combat_stats = []
        combat_stats.append(f"**AC**: {creature.ac}")
        combat_stats.append(f"**Luck (HP)**: {creature.luck}")
        combat_stats.append(f"**Attack Bonus**: +{creature.attack_bonus}")
        combat_stats.append(f"**Save DC**: {creature.save_dc}")
        combat_stats.append(f"**DPR**: {creature.dpr:.2f}")
        combat_stats.append(f"**Difficulty**: {difficulty:.2f}")
        
        if combat_stats:
            markdown_output += "### Combat Stats\n" + "  \n".join(combat_stats) + "\n\n"
        
        # Action Economy - only show non-default values
        action_economy = []
        if creature.ap != 2:
            action_economy.append(f"**AP**: {creature.ap}")
        if creature.num_attacks != 1:
            action_economy.append(f"**Number of Attacks**: {creature.num_attacks}")
        if creature.focus_points > 0:
            action_economy.append(f"**FP**: {creature.focus_points}")
        
        if action_economy:
            markdown_output += "### Action Economy\n" + "  \n".join(action_economy) + "\n\n"
        
        # Equipment Section
        has_equipment = False
        
        # Armor
        if creature.armor:
            has_equipment = True
            markdown_output += "### Armor\n"
            armor_data = armor_df[armor_df["id"] == creature.armor.armor_id].iloc[0]
            armor_cols = [col for col in armor_data.index if col not in ['id', 'cost'] and pd.notna(armor_data[col])]
            
            markdown_output += "| " + " | ".join(armor_cols) + " |\n"
            markdown_output += "|" + "|".join(["---"] * len(armor_cols)) + "|\n"
            markdown_output += "| " + " | ".join(str(armor_data[col]) for col in armor_cols) + " |\n\n"
        
        # Shield
        if creature.shield:
            has_equipment = True
            markdown_output += "### Shield\n"
            shield_data = shields_df[shields_df["id"] == creature.shield.shield_id].iloc[0]
            shield_cols = [col for col in shield_data.index if col not in ['id', 'cost'] and pd.notna(shield_data[col])]
            
            markdown_output += "| " + " | ".join(shield_cols) + " |\n"
            markdown_output += "|" + "|".join(["---"] * len(shield_cols)) + "|\n"
            markdown_output += "| " + " | ".join(str(shield_data[col]) for col in shield_cols) + " |\n\n"
        
        # Weapons
        if creature.weapons:
            has_equipment = True
            markdown_output += "### Weapons\n"
            
            # Get all possible columns from all weapon types (excluding cost)
            all_weapon_cols = set()
            for weapon in creature.weapons:
                weapon_df = weapons_df_list[weapon.weapon_type]
                weapon_data = weapon_df[weapon_df["id"] == weapon.weapon_id].iloc[0]
                cols = [col for col in weapon_data.index if col not in ['id', 'cost'] and pd.notna(weapon_data[col])]
                all_weapon_cols.update(cols)
            
            # Create header
            header_cols = ["Name", "Type"] + sorted([col for col in all_weapon_cols if col != 'name'])
            markdown_output += "| " + " | ".join(header_cols) + " |\n"
            markdown_output += "|" + "|".join(["---"] * len(header_cols)) + "|\n"
            
            # Add each weapon as a row
            for weapon in creature.weapons:
                weapon_type_name = ["Melee", "Projectile", "Firearms"][weapon.weapon_type]
                weapon_df = weapons_df_list[weapon.weapon_type]
                weapon_data = weapon_df[weapon_df["id"] == weapon.weapon_id].iloc[0]
                
                row_data = [weapon.name, weapon_type_name]
                for col in header_cols[2:]:  # Skip Name and Type columns
                    if col in weapon_data and pd.notna(weapon_data[col]):
                        row_data.append(str(weapon_data[col]))
                    else:
                        row_data.append("-")
                
                markdown_output += "| " + " | ".join(row_data) + " |\n"
            markdown_output += "\n"
        
        # Explosives
        if creature.explosives:
            has_equipment = True
            markdown_output += "### Explosives\n"
            
            # Get all possible columns from explosives (excluding cost)
            all_explosive_cols = set()
            for explosive, count in creature.explosives:
                explosive_data = explosives_df[explosives_df["id"] == explosive.explosive_id].iloc[0]
                cols = [col for col in explosive_data.index if col not in ['id', 'cost'] and pd.notna(explosive_data[col])]
                all_explosive_cols.update(cols)
            
            # Create header
            header_cols = ["Name", "Count"] + sorted([col for col in all_explosive_cols if col != 'name'])
            markdown_output += "| " + " | ".join(header_cols) + " |\n"
            markdown_output += "|" + "|".join(["---"] * len(header_cols)) + "|\n"
            
            # Add each explosive as a row
            for explosive, count in creature.explosives:
                explosive_data = explosives_df[explosives_df["id"] == explosive.explosive_id].iloc[0]
                
                row_data = [explosive.name, str(count)]
                for col in header_cols[2:]:  # Skip Name and Count columns
                    if col in explosive_data and pd.notna(explosive_data[col]):
                        row_data.append(str(explosive_data[col]))
                    else:
                        row_data.append("-")
                
                markdown_output += "| " + " | ".join(row_data) + " |\n"
            markdown_output += "\n"
        
        # Abilities - only show if there are any
        if creature.abilties:
            markdown_output += "### Abilities\n"
            for ability in creature.abilties:
                markdown_output += f"**{ability.name}** ({ability.type}, {ability.points} points)\n"
                markdown_output += f"{ability.description}\n\n"
        
        # Display the formatted output in a text box
        st.subheader("Formatted Creature Stats")
        st.text_area("Creature Statistics", markdown_output, height=600)